"""Measure real download throughput through temporary Mihomo proxy tunnels."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

import requests
import yaml

SPEED_URL = os.environ.get("SPEED_TEST_URL", "https://speed.cloudflare.com/__down?bytes=1048576")
MAX_TEST_BYTES = int(os.environ.get("SPEED_TEST_BYTES", "524288"))
MAX_PER_PROTOCOL = int(os.environ.get("MAX_SPEED_CANDIDATES_PER_PROTOCOL", "160"))
PROBE_WORKERS = int(os.environ.get("SPEED_TEST_WORKERS", "24"))
SUPPORTED = {"vmess", "vless", "trojan", "ss", "ssr", "socks", "socks5", "http", "hysteria2", "hy2", "wireguard"}


def _candidate_pool(nodes: list[dict[str, Any]], latencies: dict[tuple[str, int], float | None],
                    per_protocol: int) -> list[dict[str, Any]]:
    from collector import PROTOCOL_FEEDS, endpoint_key, stable_key

    pool: dict[str, dict[str, Any]] = {}
    for schemes in PROTOCOL_FEEDS.values():
        eligible = [node for node in nodes if str(node.get("type", "")).lower() in schemes]
        eligible.sort(key=lambda node: (
            latencies.get(endpoint_key(node)) is None if endpoint_key(node) else True,
            latencies.get(endpoint_key(node)) if endpoint_key(node) and latencies.get(endpoint_key(node)) is not None else float("inf"),
            stable_key(node),
        ))
        for node in eligible[:per_protocol]:
            if str(node.get("type", "")).lower() in SUPPORTED:
                pool.setdefault(stable_key(node), node)
    print(f"Real tunnel download test candidates: {len(pool)}")
    return list(pool.values())


def measure_download_speeds(
    nodes: list[dict[str, Any]], latencies: dict[tuple[str, int], float | None],
) -> dict[str, float]:
    """Return nodes that downloaded a real file through their own local proxy tunnel."""
    from collector import stable_key

    mihomo = shutil.which("mihomo")
    if not mihomo:
        raise RuntimeError("Mihomo is required for real tunnel speed ranking")
    candidates = _candidate_pool(nodes, latencies, MAX_PER_PROTOCOL)
    if not candidates:
        return {}

    proxies: list[dict[str, Any]] = []
    listeners: list[dict[str, Any]] = []
    ports: dict[str, int] = {}
    key_by_name: dict[str, str] = {}
    names: set[str] = set()
    for index, original in enumerate(candidates):
        node = dict(original)
        kind = str(node.get("type", "")).lower()
        if kind not in SUPPORTED:
            continue
        if kind == "hy2":
            node["type"] = "hysteria2"
        base = str(node.get("name") or f"{kind}-{index}")
        name, suffix = base, 2
        while name in names:
            name = f"{base}-{suffix}"
            suffix += 1
        names.add(name)
        node["name"] = name
        port = 30000 + len(proxies)
        proxies.append(node)
        listeners.append({"name": f"bench-{index}", "type": "socks", "port": port,
                          "listen": "127.0.0.1", "proxy": name})
        ports[stable_key(original)] = port
        key_by_name[name] = stable_key(original)

    config = {"mixed-port": 0, "allow-lan": False, "mode": "rule", "log-level": "silent",
              "ipv6": True, "proxies": proxies, "listeners": listeners, "rules": ["MATCH,DIRECT"]}
    with tempfile.TemporaryDirectory(prefix="node-speed-") as temp_dir:
        config_path = Path(temp_dir) / "config.yaml"
        config_path.write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False), encoding="utf-8")
        checked = subprocess.run([mihomo, "-t", "-d", temp_dir, "-f", str(config_path)],
                                 capture_output=True, text=True, timeout=45)
        if checked.returncode:
            print("Mihomo rejected the combined candidate config; validating proxies one by one")
            valid_proxies, valid_listeners = [], []
            for proxy_node, listener in zip(proxies, listeners):
                single_config = {**config, "proxies": [proxy_node], "listeners": [listener]}
                config_path.write_text(yaml.safe_dump(single_config, allow_unicode=True, sort_keys=False), encoding="utf-8")
                try:
                    single_check = subprocess.run([mihomo, "-t", "-d", temp_dir, "-f", str(config_path)],
                                                  capture_output=True, text=True, timeout=10)
                except subprocess.TimeoutExpired:
                    continue
                if single_check.returncode == 0:
                    valid_proxies.append(proxy_node)
                    valid_listeners.append(listener)
                else:
                    print(f"SKIP_SPEED_CANDIDATE\t{proxy_node.get('name', '')}\tinvalid Mihomo config")
            if not valid_proxies:
                print(f"Mihomo could not validate any candidates: {checked.stderr[-1000:]}")
                return {}
            proxies, listeners = valid_proxies, valid_listeners
            valid_names = {proxy_node["name"] for proxy_node in proxies}
            ports = {key: port for key, port in ports.items()
                     if any(key_by_name.get(name) == key for name in valid_names)}
            config.update(proxies=proxies, listeners=listeners)
            config_path.write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False), encoding="utf-8")
            checked = subprocess.run([mihomo, "-t", "-d", temp_dir, "-f", str(config_path)],
                                     capture_output=True, text=True, timeout=45)
            if checked.returncode:
                raise RuntimeError(f"Mihomo rejected filtered test config: {checked.stderr[-1500:]} {checked.stdout[-500:]}")
        with open(os.devnull, "w", encoding="utf-8") as sink:
            process = subprocess.Popen([mihomo, "-d", temp_dir, "-f", str(config_path)],
                                       stdout=sink, stderr=sink)
            try:
                time.sleep(2)
                if process.poll() is not None:
                    raise RuntimeError("Mihomo exited before tunnel probes started")

                def download(item: tuple[str, int]) -> tuple[str, float | None, int]:
                    key, port = item
                    session = requests.Session()
                    proxy = f"socks5h://127.0.0.1:{port}"
                    session.trust_env = False
                    started = time.perf_counter()
                    count = 0
                    try:
                        with session.get(SPEED_URL, proxies={"http": proxy, "https": proxy},
                                         stream=True, timeout=(4, 8)) as response:
                            response.raise_for_status()
                            for chunk in response.iter_content(chunk_size=64 * 1024):
                                if chunk:
                                    count += len(chunk)
                                    if count >= MAX_TEST_BYTES:
                                        break
                        elapsed = time.perf_counter() - started
                        if count < min(256 * 1024, MAX_TEST_BYTES):
                            return key, None, count
                        return key, count * 8 / elapsed / 1_000_000, count
                    except requests.RequestException:
                        return key, None, count
                    finally:
                        session.close()

                speeds: dict[str, float] = {}
                with ThreadPoolExecutor(max_workers=PROBE_WORKERS) as executor:
                    futures = [executor.submit(download, item) for item in ports.items()]
                    for future in as_completed(futures):
                        key, speed, amount = future.result()
                        if speed is not None:
                            speeds[key] = speed
                            print(f"DOWNLOAD_SPEED\t{key}\t{speed:.3f} Mbps\t{amount} bytes")
                print(f"Real tunnel download tests succeeded: {len(speeds)}/{len(ports)}")
                return speeds
            finally:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()

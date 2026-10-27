#!/usr/bin/env python3
"""Fetch public proxy subscriptions and publish V2Ray, Clash, and SS/SSR feeds."""

from __future__ import annotations

import base64
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent
SOURCES_FILE = Path(os.environ.get("SOURCES_FILE", ROOT / "sources.txt"))
OUTPUT = Path(os.environ.get("OUTPUT_DIR", ROOT / "subscriptions"))
MAX_BYTES = int(os.environ.get("MAX_SOURCE_BYTES", str(5 * 1024 * 1024)))
TIMEOUT = int(os.environ.get("FETCH_TIMEOUT", "20"))
USER_AGENT = "FreeVPN-Node-Aggregator/1.0 (public subscription parser)"
SCHEMES = {"vmess", "vless", "trojan", "ss", "ssr"}


def decode_b64(value: str) -> bytes | None:
    value = re.sub(r"\s+", "", value)
    if not value:
        return None
    try:
        return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))
    except (ValueError, base64.binascii.Error):
        return None


def decode_text(data: bytes) -> str:
    return data.decode("utf-8-sig", errors="replace").strip()


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError(f"source exceeds {MAX_BYTES} bytes")
    return data


def canonical_uri(uri: str) -> str | None:
    uri = uri.strip().strip("\"'")
    if not uri:
        return None
    scheme = uri.partition(":")[0].lower()
    if scheme not in SCHEMES:
        return None
    if scheme == "ssr":
        return uri if decode_b64(uri[len("ssr://"):]) else None
    if scheme == "vmess":
        payload = decode_b64(uri.partition("://")[2])
        if payload:
            try:
                obj = json.loads(payload)
                host, port, uid = str(obj.get("add", "")).strip(), str(obj.get("port", "")), str(obj.get("id", ""))
                if host and port and uid:
                    normalized = dict(obj)
                    normalized["add"], normalized["port"], normalized["id"] = host, port, uid
                    return "vmess://" + base64.urlsafe_b64encode(json.dumps(normalized, separators=(",", ":")).encode()).decode().rstrip("=")
            except (ValueError, TypeError):
                pass
        return uri
    # URL parsing validates common userinfo/host forms while keeping original parameters.
    try:
        parsed = urllib.parse.urlsplit(uri)
        if not parsed.hostname:
            return None
        if parsed.port is not None and not (1 <= parsed.port <= 65535):
            return None
        return uri
    except ValueError:
        return None


def uri_items(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    # Some sources wrap all URI lines in a single base64 subscription.
    if "://" not in text and not text.lstrip().startswith(("proxies:", "proxy-groups:", "port:", "mixed-port:")):
        decoded = decode_b64(text)
        if decoded:
            candidate = decode_text(decoded)
            if "://" in candidate or candidate.lstrip().startswith(("proxies:", "proxies :")):
                text = candidate
    return [line.strip().strip("\"'") for line in text.splitlines() if "://" in line]


def from_clash(document: Any) -> list[dict[str, Any]]:
    if not isinstance(document, dict) or not isinstance(document.get("proxies"), list):
        return []
    nodes = []
    for value in document["proxies"]:
        if not isinstance(value, dict) or str(value.get("type", "")).lower() not in SCHEMES:
            continue
        node = dict(value)
        node["name"] = str(node.get("name") or f"{node['type']}-{node.get('server', 'node')}")
        nodes.append(node)
    return nodes


def parse_ss(uri: str) -> dict[str, Any] | None:
    body, _, fragment = uri.partition("#")
    authority = body[len("ss://"):]
    # SIP002: method:password@host:port, optionally base64 wrapped.
    if "@" not in authority:
        decoded = decode_b64(authority.split("?", 1)[0])
        if decoded:
            authority = decode_text(decoded)
    if "@" not in authority:
        return None
    credentials, address = authority.rsplit("@", 1)
    decoded_credentials = decode_b64(credentials)
    if decoded_credentials and b":" in decoded_credentials:
        candidate = decode_text(decoded_credentials)
        if "\ufffd" not in candidate and candidate.isprintable():
            credentials = candidate
    method, sep, password = credentials.partition(":")
    try:
        parsed = urllib.parse.urlsplit("//" + address)
        if not (sep and method and password and parsed.hostname and parsed.port):
            return None
    except ValueError:
        return None
    return {"name": urllib.parse.unquote(fragment) or f"ss-{parsed.hostname}", "type": "ss", "server": parsed.hostname,
            "port": parsed.port, "cipher": method, "password": password}


def parse_ssr(uri: str) -> dict[str, Any] | None:
    payload = decode_b64(uri[len("ssr://"):])
    if not payload:
        return None
    core = decode_text(payload).split("/?", 1)[0]
    fields = core.split(":", 5)
    if len(fields) != 6:
        return None
    server, port, protocol, method, obfs, password64 = fields
    password = decode_text(decode_b64(password64) or b"")
    if not (server and port.isdigit() and protocol and method and obfs and password):
        return None
    return {"name": f"ssr-{server}", "type": "ssr", "server": server, "port": int(port),
            "cipher": method, "password": password, "protocol": protocol, "obfs": obfs}


def from_uri(uri: str) -> dict[str, Any] | None:
    uri = canonical_uri(uri)
    if not uri:
        return None
    scheme = uri.partition(":")[0].lower()
    if scheme == "ss":
        return parse_ss(uri)
    if scheme == "ssr":
        return parse_ssr(uri)
    if scheme == "vmess":
        raw = decode_b64(uri[len("vmess://"):])
        if not raw:
            return None
        try:
            value = json.loads(raw)
            server, port = str(value.get("add", "")), str(value.get("port", ""))
            if not server or not port.isdigit():
                return None
            tls = str(value.get("tls", "")).lower() == "tls"
            net = str(value.get("net", "tcp")).lower()
            node: dict[str, Any] = {"name": str(value.get("ps") or f"vmess-{server}"), "type": "vmess",
                "server": server, "port": int(port), "uuid": str(value.get("id", "")),
                "alterId": int(value.get("aid", 0) or 0), "cipher": "auto", "udp": True,
                "tls": tls, "network": net}
            if net == "ws":
                node["ws-opts"] = {"path": str(value.get("path", "/")), "headers": {"Host": str(value.get("host", ""))}}
            elif net == "grpc":
                node["grpc-opts"] = {"grpc-service-name": str(value.get("path", ""))}
            if tls and value.get("sni"):
                node["servername"] = value["sni"]
            return node if node["uuid"] else None
        except (ValueError, TypeError):
            return None
    try:
        parsed = urllib.parse.urlsplit(uri)
        if not parsed.hostname or not parsed.port:
            return None
        name = urllib.parse.unquote(parsed.fragment) or f"{scheme}-{parsed.hostname}"
        query = urllib.parse.parse_qs(parsed.query)
        if scheme == "vless":
            node = {"name": name, "type": "vless", "server": parsed.hostname, "port": parsed.port,
                    "uuid": urllib.parse.unquote(parsed.username or ""), "udp": True}
            security = query.get("security", [""])[0]
            if security in {"tls", "reality"}:
                node["tls"] = True
                node["servername"] = query.get("sni", [""])[0]
                node["client-fingerprint"] = query.get("fp", [""])[0] or "chrome"
                if security == "reality":
                    node["reality-opts"] = {"public-key": query.get("pbk", [""])[0], "short-id": query.get("sid", [""])[0]}
            network = query.get("type", ["tcp"])[0]
            node["network"] = network
            if network == "ws":
                node["ws-opts"] = {"path": query.get("path", ["/"])[0],
                                   "headers": {"Host": query.get("host", [""])[0]}}
            elif network == "grpc":
                node["grpc-opts"] = {"grpc-service-name": query.get("serviceName", [""])[0]}
            return node if node["uuid"] else None
        if scheme == "trojan":
            node = {"name": name, "type": "trojan", "server": parsed.hostname, "port": parsed.port,
                    "password": urllib.parse.unquote(parsed.username or ""), "udp": True}
            node["sni"] = query.get("sni", [""])[0]
            node["network"] = query.get("type", ["tcp"])[0]
            return node if node["password"] else None
    except ValueError:
        return None
    return None


def stable_key(node: dict[str, Any]) -> str:
    # Names are deliberately excluded so mirrors label-identically configured servers the same way.
    identity = {key: value for key, value in node.items() if key != "name"}
    payload = json.dumps(identity, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode()).hexdigest()


def load_source(url: str) -> tuple[list[str], list[dict[str, Any]]]:
    url = url.replace("{date}", datetime.now(timezone.utc).strftime("%Y%m%d"))
    raw = fetch(url)
    text = decode_text(raw)
    clash_nodes: list[dict[str, Any]] = []
    # YAML feeds can start with comments or other top-level Clash settings, so
    # do not require `proxies:` to be the first line before attempting a parse.
    try:
        clash_nodes = from_clash(yaml.safe_load(text))
    except yaml.YAMLError:
        pass
    return uri_items(text), clash_nodes


def main() -> int:
    sources = [line.strip() for line in SOURCES_FILE.read_text(encoding="utf-8").splitlines()
               if line.strip() and not line.lstrip().startswith("#")]
    if not sources:
        print("No source URLs configured", file=sys.stderr)
        return 2

    all_uris: dict[str, str] = {}
    all_nodes: dict[str, dict[str, Any]] = {}
    successes = 0
    for url in sources:
        try:
            uris, clash = load_source(url)
            found = 0
            for uri in uris:
                valid = canonical_uri(uri)
                node = from_uri(uri)
                if valid:
                    all_uris.setdefault(valid, valid)
                if node:
                    all_nodes.setdefault(stable_key(node), node)
                if valid or node:
                    found += 1
            for node in clash:
                all_nodes.setdefault(stable_key(node), node)
                found += 1
            if found:
                successes += 1
            print(f"{url}: parsed {found} entries")
        except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
            print(f"{url}: {type(exc).__name__}: {exc}", file=sys.stderr)

    if not successes:
        print("All sources failed or returned no usable entries; preserving existing feeds.", file=sys.stderr)
        return 1

    v2ray = sorted(uri for uri in all_uris.values() if uri.startswith(("vmess://", "vless://", "trojan://")))
    ss_ssr = sorted(uri for uri in all_uris.values() if uri.startswith(("ss://", "ssr://")))
    clash_nodes = sorted(all_nodes.values(), key=lambda item: (str(item.get("name", "")).casefold(), stable_key(item)))
    # Clash requires stable, unique proxy labels for groups.
    used_names: set[str] = set()
    for node in clash_nodes:
        base = str(node.get("name") or node.get("server") or node["type"])
        name, suffix = base, 2
        while name in used_names:
            name = f"{base}-{suffix}"
            suffix += 1
        node["name"] = name
        used_names.add(name)
    if not v2ray and not ss_ssr and not clash_nodes:
        print("No supported nodes were parsed; preserving existing feeds.", file=sys.stderr)
        return 1

    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "v2ray.txt").write_text(base64.b64encode("\n".join(v2ray).encode()).decode() + "\n", encoding="ascii")
    (OUTPUT / "ss-ssr.txt").write_text(base64.b64encode("\n".join(ss_ssr).encode()).decode() + "\n", encoding="ascii")
    document = {"port": 7890, "socks-port": 7891, "allow-lan": False, "mode": "rule", "log-level": "warning",
                "proxies": clash_nodes,
                "proxy-groups": [{"name": "AUTO", "type": "url-test", "proxies": [p["name"] for p in clash_nodes],
                                  "url": "https://www.gstatic.com/generate_204", "interval": 300}],
                "rules": ["MATCH,AUTO"]}
    (OUTPUT / "clash.yaml").write_text(yaml.safe_dump(document, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"Published {len(v2ray)} V2Ray-family URIs, {len(ss_ssr)} SS/SSR URIs, {len(clash_nodes)} Clash nodes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

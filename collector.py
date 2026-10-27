#!/usr/bin/env python3
"""Fetch public proxy subscriptions and publish protocol-specific feeds."""

from __future__ import annotations

import base64
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor
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
SCHEMES = {"vmess", "vless", "trojan", "ss", "ssr", "hysteria2", "hy2", "socks", "socks5", "http", "https", "wireguard"}
PROTOCOL_FEEDS = {
    "vmess": ("vmess",), "vless": ("vless",), "ss": ("ss",), "ssr": ("ssr",),
    "socks": ("socks", "socks5"), "http": ("http", "https"),
    "trojan": ("trojan",), "wireguard": ("wireguard",),
    "hysteria2": ("hysteria2", "hy2"),
}


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


def endpoint_uri_items(text: str, scheme: str, limit: int = 2500) -> list[str]:
    """Convert a bounded plain host:port proxy list into share links."""
    if scheme not in {"http", "socks5"}:
        return []
    results: list[str] = []
    seen: set[str] = set()
    for line in text.splitlines():
        value = line.strip().strip("\"'")
        if not value or value.startswith(("#", "//")) or "://" in value or any(ch.isspace() for ch in value):
            continue
        try:
            parsed = urllib.parse.urlsplit("//" + value)
            host, port = parsed.hostname, parsed.port
        except ValueError:
            continue
        if not host or not port or not (1 <= port <= 65535):
            continue
        authority_host = f"[{host}]" if ":" in host and not host.startswith("[") else host
        uri = f"{scheme}://{authority_host}:{port}"
        if uri not in seen:
            results.append(uri)
            seen.add(uri)
        if len(results) >= limit:
            break
    return results

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
        if scheme in {"socks", "socks5", "http", "https"}:
            kind = "socks5" if scheme in {"socks", "socks5"} else "http"
            node = {"name": name, "type": kind, "server": parsed.hostname, "port": parsed.port, "udp": True}
            if parsed.username is not None:
                username = urllib.parse.unquote(parsed.username)
                password = urllib.parse.unquote(parsed.password or "")
                decoded_auth = decode_b64(username) if not password else None
                if decoded_auth != b":":
                    if username:
                        node["username"] = username
                    if password:
                        node["password"] = password
            if scheme == "https" or query.get("tls", [""])[0].lower() == "true":
                node["tls"] = True
            return node
        if scheme == "wireguard":
            private_key = urllib.parse.unquote(parsed.username or "")
            public_key = query.get("publickey", query.get("public-key", [""]))[0]
            address = query.get("address", query.get("ip", [""]))[0]
            if not (private_key and public_key and address):
                return None
            node = {"name": name, "type": "wireguard", "server": parsed.hostname, "port": parsed.port,
                    "private-key": private_key, "public-key": public_key, "ip": address, "udp": True}
            if query.get("presharedkey", [""])[0]:
                node["preshared-key"] = query["presharedkey"][0]
            if query.get("reserved", [""])[0]:
                try:
                    node["reserved"] = [int(part) for part in query["reserved"][0].split(",")]
                except ValueError:
                    return None
            if query.get("mtu", [""])[0].isdigit():
                node["mtu"] = int(query["mtu"][0])
            return node
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
        if scheme in {"hysteria2", "hy2"}:
            password = urllib.parse.unquote(parsed.username or "")
            if not password:
                return None
            node = {"name": name, "type": "hysteria2", "server": parsed.hostname, "port": parsed.port,
                    "password": password, "udp": True}
            for key in ("sni", "obfs", "obfs-password"):
                if query.get(key, [""])[0]:
                    node[key] = query[key][0]
            return node
        if scheme == "trojan":
            node = {"name": name, "type": "trojan", "server": parsed.hostname, "port": parsed.port,
                    "password": urllib.parse.unquote(parsed.username or ""), "udp": True}
            node["sni"] = query.get("sni", [""])[0]
            node["network"] = query.get("type", ["tcp"])[0]
            return node if node["password"] else None
    except ValueError:
        return None
    return None


def uri_from_node(node: dict[str, Any]) -> str | None:
    """Convert supported Clash/Xray node dictionaries back to share-link formats."""
    kind = str(node.get("type", "")).lower()
    server = str(node.get("server", ""))
    port = str(node.get("port", ""))
    name = str(node.get("name") or f"{kind}-{server}")
    if not server or not port:
        return None
    host = f"[{server}]" if ":" in server and not server.startswith("[") else server
    label = urllib.parse.quote(name, safe="")
    network = str(node.get("network", "tcp"))
    ws = node.get("ws-opts", {}) if isinstance(node.get("ws-opts"), dict) else {}
    ws_headers = ws.get("headers", {}) if isinstance(ws.get("headers"), dict) else {}
    grpc = node.get("grpc-opts", {}) if isinstance(node.get("grpc-opts"), dict) else {}

    if kind == "vmess":
        value = {"v": "2", "ps": name, "add": server, "port": port,
                 "id": str(node.get("uuid", "")), "aid": str(node.get("alterId", 0)),
                 "scy": str(node.get("cipher", "auto")), "net": network, "type": "none",
                 "host": str(ws_headers.get("Host", "")), "path": str(ws.get("path", grpc.get("grpc-service-name", "/"))),
                 "tls": "tls" if node.get("tls") else ""}
        if node.get("servername"):
            value["sni"] = str(node["servername"])
        if not value["id"]:
            return None
        payload = base64.b64encode(json.dumps(value, separators=(",", ":"), ensure_ascii=False).encode()).decode()
        return "vmess://" + payload

    if kind == "vless":
        uid = str(node.get("uuid", ""))
        if not uid:
            return None
        params: dict[str, str] = {"encryption": "none", "type": network}
        reality = node.get("reality-opts", {}) if isinstance(node.get("reality-opts"), dict) else {}
        if reality:
            params["security"] = "reality"
            if reality.get("public-key"):
                params["pbk"] = str(reality["public-key"])
            if reality.get("short-id"):
                params["sid"] = str(reality["short-id"])
        elif node.get("tls"):
            params["security"] = "tls"
        sni = node.get("servername") or node.get("sni")
        if sni:
            params["sni"] = str(sni)
        if node.get("client-fingerprint"):
            params["fp"] = str(node["client-fingerprint"])
        if node.get("flow"):
            params["flow"] = str(node["flow"])
        if network == "ws":
            params["path"] = str(ws.get("path", "/"))
            if ws_headers.get("Host"):
                params["host"] = str(ws_headers["Host"])
        elif network == "grpc" and grpc.get("grpc-service-name"):
            params["serviceName"] = str(grpc["grpc-service-name"])
        return f"vless://{urllib.parse.quote(uid, safe='')}@{host}:{port}?{urllib.parse.urlencode(params)}#{label}"

    if kind == "trojan":
        password = str(node.get("password", ""))
        if not password:
            return None
        params = {"security": "tls" if node.get("tls", True) else "none", "type": network}
        sni = node.get("sni") or node.get("servername")
        if sni:
            params["sni"] = str(sni)
        if network == "ws":
            params["path"] = str(ws.get("path", "/"))
            if ws_headers.get("Host"):
                params["host"] = str(ws_headers["Host"])
        elif network == "grpc" and grpc.get("grpc-service-name"):
            params["serviceName"] = str(grpc["grpc-service-name"])
        return f"trojan://{urllib.parse.quote(password, safe='')}@{host}:{port}?{urllib.parse.urlencode(params)}#{label}"

    if kind in {"hysteria2", "hy2"}:
        password = str(node.get("password", ""))
        if not password:
            return None
        params = {}
        for key in ("sni", "obfs", "obfs-password"):
            if node.get(key):
                params[key] = str(node[key])
        query = "?" + urllib.parse.urlencode(params) if params else ""
        return f"hysteria2://{urllib.parse.quote(password, safe='')}@{host}:{port}{query}#{label}"
    if kind in {"socks", "socks5", "http"}:
        scheme = "socks5" if kind in {"socks", "socks5"} else ("https" if node.get("tls") else "http")
        username = str(node.get("username", ""))
        password = str(node.get("password", ""))
        credentials = ""
        if username:
            credentials = urllib.parse.quote(username, safe="")
            if password:
                credentials += ":" + urllib.parse.quote(password, safe="")
            credentials += "@"
        return f"{scheme}://{credentials}{host}:{port}#{label}"

    if kind == "wireguard":
        private_key = str(node.get("private-key", node.get("private_key", "")))
        public_key = str(node.get("public-key", node.get("public_key", "")))
        address = str(node.get("ip", node.get("address", "")))
        if not (private_key and public_key and address):
            return None
        params = {"address": address, "publickey": public_key}
        if node.get("preshared-key") or node.get("preshared_key"):
            params["presharedkey"] = str(node.get("preshared-key", node.get("preshared_key")))
        if node.get("reserved") is not None:
            reserved = node["reserved"]
            params["reserved"] = ",".join(str(x) for x in reserved) if isinstance(reserved, list) else str(reserved)
        if node.get("mtu"):
            params["mtu"] = str(node["mtu"])
        return f"wireguard://{urllib.parse.quote(private_key, safe='')}@{host}:{port}?{urllib.parse.urlencode(params)}#{label}"
    if kind == "ss":
        method, password = str(node.get("cipher", "")), str(node.get("password", ""))
        if not method or not password:
            return None
        auth = base64.b64encode(f"{method}:{password}".encode()).decode().rstrip("=")
        return f"ss://{auth}@{host}:{port}#{label}"

    if kind == "ssr":
        method, password = str(node.get("cipher", "")), str(node.get("password", ""))
        protocol, obfs = str(node.get("protocol", "")), str(node.get("obfs", ""))
        if not method or not password or not protocol or not obfs:
            return None
        b64 = lambda value: base64.urlsafe_b64encode(value.encode()).decode().rstrip("=")
        core = f"{server}:{port}:{protocol}:{method}:{obfs}:{b64(password)}"
        params = []
        if node.get("obfs-param"):
            params.append("obfsparam=" + b64(str(node["obfs-param"])))
        if node.get("protocol-param"):
            params.append("protoparam=" + b64(str(node["protocol-param"])))
        params.append("remarks=" + b64(name))
        return "ssr://" + b64(core + "/?" + "&".join(params))
    return None


def from_xray(document: Any) -> list[dict[str, Any]]:
    """Extract proxy outbounds from an Xray JSON client configuration."""
    if not isinstance(document, dict) or not isinstance(document.get("outbounds"), list):
        return []
    nodes: list[dict[str, Any]] = []
    for outbound in document["outbounds"]:
        if not isinstance(outbound, dict):
            continue
        kind = str(outbound.get("protocol", "")).lower()
        settings = outbound.get("settings", {})
        stream = outbound.get("streamSettings", {})
        if not isinstance(settings, dict) or not isinstance(stream, dict):
            continue
        network = str(stream.get("network", "tcp"))
        security = str(stream.get("security", "")).lower()
        tls = stream.get("tlsSettings", {}) if isinstance(stream.get("tlsSettings"), dict) else {}
        reality = stream.get("realitySettings", {}) if isinstance(stream.get("realitySettings"), dict) else {}
        base: dict[str, Any] = {"type": kind, "name": str(outbound.get("tag") or f"{kind}-node"),
                                 "network": network, "udp": True}
        if security in {"tls", "reality"}:
            base["tls"] = True
            base["servername"] = str(tls.get("serverName") or reality.get("serverName") or "")
            if security == "reality":
                base["reality-opts"] = {"public-key": str(reality.get("publicKey", "")),
                                        "short-id": str(reality.get("shortId", ""))}
                if reality.get("fingerprint"):
                    base["client-fingerprint"] = str(reality["fingerprint"])
            elif tls.get("fingerprint"):
                base["client-fingerprint"] = str(tls["fingerprint"])
        ws = stream.get("wsSettings", {}) if isinstance(stream.get("wsSettings"), dict) else {}
        if network == "ws":
            headers = ws.get("headers", {}) if isinstance(ws.get("headers"), dict) else {}
            base["ws-opts"] = {"path": str(ws.get("path", "/")), "headers": {"Host": str(headers.get("Host", ""))}}
        grpc = stream.get("grpcSettings", {}) if isinstance(stream.get("grpcSettings"), dict) else {}
        if network == "grpc":
            base["grpc-opts"] = {"grpc-service-name": str(grpc.get("serviceName", ""))}

        if kind in {"vless", "vmess"}:
            servers = settings.get("vnext", [])
            for server in servers if isinstance(servers, list) else []:
                if not isinstance(server, dict) or not server.get("address") or not server.get("port"):
                    continue
                for user in server.get("users", []):
                    if not isinstance(user, dict) or not user.get("id"):
                        continue
                    node = {**base, "server": str(server["address"]), "port": int(server["port"]), "uuid": str(user["id"])}
                    if kind == "vmess":
                        node["alterId"] = int(user.get("alterId", 0) or 0)
                        node["cipher"] = str(user.get("security", "auto") or "auto")
                    elif user.get("flow"):
                        node["flow"] = str(user["flow"])
                    nodes.append(node)
        elif kind in {"trojan", "shadowsocks"}:
            for server in settings.get("servers", []) if isinstance(settings.get("servers", []), list) else []:
                if not isinstance(server, dict) or not server.get("address") or not server.get("port"):
                    continue
                node = {**base, "type": "ss" if kind == "shadowsocks" else "trojan",
                        "server": str(server["address"]), "port": int(server["port"])}
                if kind == "trojan":
                    node["password"] = str(server.get("password", ""))
                    node["sni"] = base.get("servername", "")
                else:
                    node["cipher"] = str(server.get("method", ""))
                    node["password"] = str(server.get("password", ""))
                if node.get("password"):
                    nodes.append(node)
    return nodes

def stable_key(node: dict[str, Any]) -> str:
    # Names are deliberately excluded so mirrors label-identically configured servers the same way.
    identity = {key: value for key, value in node.items() if key != "name"}
    payload = json.dumps(identity, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode()).hexdigest()


def endpoint_key(node: dict[str, Any]) -> tuple[str, int] | None:
    host, port = str(node.get("server", "")).strip(), node.get("port")
    try:
        port_number = int(port)
    except (TypeError, ValueError):
        return None
    if not host or not 1 <= port_number <= 65535:
        return None
    return host.lower().strip("[]"), port_number


def probe_tcp(endpoint: tuple[str, int]) -> tuple[tuple[str, int], float | None]:
    """Measure TCP connect latency in milliseconds; None means unreachable/timeout."""
    started = time.perf_counter()
    try:
        with socket.create_connection(endpoint, timeout=1.5):
            return endpoint, (time.perf_counter() - started) * 1000
    except (OSError, UnicodeError, OverflowError, ValueError):
        return endpoint, None


def measure_latencies(nodes: list[dict[str, Any]]) -> dict[tuple[str, int], float | None]:
    endpoints = sorted({key for node in nodes if (key := endpoint_key(node)) is not None})
    with ThreadPoolExecutor(max_workers=256) as pool:
        results = dict(pool.map(probe_tcp, endpoints))
    reachable = sum(value is not None for value in results.values())
    print(f"TCP latency probes: {reachable}/{len(endpoints)} endpoints reachable")
    return results


def latency_sort_key(node: dict[str, Any], latencies: dict[tuple[str, int], float | None]) -> tuple[bool, float, str]:
    endpoint = endpoint_key(node)
    latency = latencies.get(endpoint) if endpoint else None
    return latency is None, latency if latency is not None else float("inf"), stable_key(node)


def log_latency_results(group: str, nodes: list[dict[str, Any]], latencies: dict[tuple[str, int], float | None]) -> None:
    for rank, node in enumerate(nodes, 1):
        endpoint = endpoint_key(node)
        value = latencies.get(endpoint) if endpoint else None
        milliseconds = f"{value:.2f}" if value is not None else "unreachable"
        server = f"{endpoint[0]}:{endpoint[1]}" if endpoint else "unknown"
        name = str(node.get("name", "")).replace("\t", " ").replace("\r", " ").replace("\n", " ")
        print(f"LATENCY_RESULT\t{group}\t{rank}\t{milliseconds}\t{node.get('type', '')}\t{server}\t{name}")
def load_source(url: str, raw_proxy_type: str | None = None) -> tuple[list[str], list[dict[str, Any]]]:
    url = url.replace("{date}", datetime.now(timezone.utc).strftime("%Y%m%d"))
    raw = fetch(url)
    text = decode_text(raw)
    clash_nodes: list[dict[str, Any]] = []
    try:
        document = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        try:
            document = yaml.safe_load(text)
        except yaml.YAMLError:
            document = None
    if isinstance(document, dict) and isinstance(document.get("proxies"), list):
        clash_nodes = from_clash(document)
    elif isinstance(document, dict) and isinstance(document.get("outbounds"), list):
        clash_nodes = from_xray(document)
    uris = uri_items(text)
    if raw_proxy_type:
        uris.extend(endpoint_uri_items(text, raw_proxy_type))
    return uris, clash_nodes

def update_readme_node_lists(protocol_links: dict[str, list[str]], clash_nodes: list[dict[str, Any]]) -> None:
    """Keep stable main and backup URLs plus generated node snapshots in README."""
    readme_path = ROOT / "README.md"
    labels = {
        "v2ray": "V2Ray (VMess + VLESS + Trojan)", "ss-ssr": "SS / SSR",
        "clash": "Clash / Mihomo", "vmess": "VMess", "vless": "VLESS",
        "ss": "Shadowsocks", "ssr": "ShadowsocksR", "socks": "SOCKS", "http": "HTTP",
        "trojan": "Trojan", "wireguard": "WireGuard", "hysteria2": "Hysteria2",
    }
    order = ("v2ray", "ss-ssr", "clash", "vmess", "vless", "ss", "ssr", "socks", "http", "trojan", "wireguard", "hysteria2")
    lines = ["# Subscriptions", "", "## Primary URLs"]
    for key in order:
        extension = "yaml" if key == "clash" else "txt"
        lines.append(f"- {labels[key]}: https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/{key}.{extension}")
    lines.extend(["", "## Backup URLs"])
    for key in order:
        extension = "yaml" if key == "clash" else "txt"
        lines.append(f"- {labels[key]}: https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/{key}.{extension}")
    lines.extend(["", "<!-- GENERATED-NODES:START -->", "## Current nodes",
                  "At most 30 nodes per feed, sorted by TCP connection time measured from GitHub Actions. WireGuard and Hysteria2 use UDP; TCP connection time is only a port reachability reference, not UDP handshake or VPN tunnel latency."])
    for key in order:
        if key == "clash":
            content = yaml.safe_dump({"proxies": clash_nodes}, allow_unicode=True, sort_keys=False).rstrip() if clash_nodes else "proxies: []"
            fence = "yaml"
        else:
            values = protocol_links.get(key, [])
            content = "\n".join(values) if values else "(No usable nodes this round)"
            fence = "text"
        lines.extend(["", f"### {labels[key]}", f"```{fence}", content, "```"])
    lines.append("<!-- GENERATED-NODES:END -->")
    readme_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
def main() -> int:
    source_lines = [line.strip() for line in SOURCES_FILE.read_text(encoding="utf-8").splitlines()
                    if line.strip() and not line.lstrip().startswith("#")]
    sources: list[tuple[str, str | None]] = []
    for line in source_lines:
        if "|" in line:
            raw_proxy_type, url = line.split("|", 1)
            if raw_proxy_type not in {"http", "socks5"}:
                print(f"Unsupported raw proxy type in source entry: {raw_proxy_type}", file=sys.stderr)
                continue
            sources.append((url.strip(), raw_proxy_type))
        else:
            sources.append((line, None))
    if not sources:
        print("No source URLs configured", file=sys.stderr)
        return 2

    all_uris: dict[str, str] = {}
    all_nodes: dict[str, dict[str, Any]] = {}
    successes = 0

    def fetch_one(source: tuple[str, str | None]) -> tuple[str, list[str], list[dict[str, Any]], Exception | None]:
        url, raw_proxy_type = source
        try:
            uris, clash = load_source(url, raw_proxy_type)
            return url, uris, clash, None
        except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
            return url, [], [], exc

    with ThreadPoolExecutor(max_workers=16) as source_pool:
        for url, uris, clash, error in source_pool.map(fetch_one, sources):
            if error is not None:
                print(f"{url}: {type(error).__name__}: {error}", file=sys.stderr)
                continue
            found = 0
            for uri in uris:
                # Publish only links that the client-format parser can fully parse.
                node = from_uri(uri)
                valid = canonical_uri(uri) if node else None
                if valid and node:
                    all_uris.setdefault(valid, valid)
                    all_nodes.setdefault(stable_key(node), node)
                    found += 1
            for node in clash:
                all_nodes.setdefault(stable_key(node), node)
                share = uri_from_node(node)
                if share:
                    normalized = canonical_uri(share)
                    if normalized:
                        all_uris.setdefault(normalized, normalized)
                found += 1
            if found:
                successes += 1
            print(f"{url}: parsed {found} entries")
    if not successes:
        print("All sources failed or returned no usable entries; preserving existing feeds.", file=sys.stderr)
        return 1

    latencies = measure_latencies(list(all_nodes.values()))

    def uri_latency_key(uri: str) -> tuple[bool, float, str]:
        node = from_uri(uri)
        return latency_sort_key(node, latencies) if node else (True, float("inf"), uri)

    protocol_links: dict[str, list[str]] = {}
    for feed, accepted_schemes in PROTOCOL_FEEDS.items():
        protocol_links[feed] = sorted(
            (uri for uri in all_uris.values() if uri.partition(":")[0].lower() in accepted_schemes),
            key=uri_latency_key,
        )[:30]
    v2ray = sorted(
        (uri for uri in all_uris.values() if uri.startswith(("vmess://", "vless://", "trojan://"))),
        key=uri_latency_key,
    )[:30]
    ss_ssr = sorted(
        (uri for uri in all_uris.values() if uri.startswith(("ss://", "ssr://"))),
        key=uri_latency_key,
    )[:30]
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
    clash_nodes.sort(key=lambda item: latency_sort_key(item, latencies))
    clash_nodes = clash_nodes[:30]
    log_latency_results("V2Ray", [node for uri in v2ray if (node := from_uri(uri)) is not None], latencies)
    log_latency_results("SS-SSR", [node for uri in ss_ssr if (node := from_uri(uri)) is not None], latencies)
    log_latency_results("Clash", clash_nodes, latencies)
    for feed, links in protocol_links.items():
        log_latency_results(feed, [node for uri in links if (node := from_uri(uri)) is not None], latencies)
    if not v2ray and not ss_ssr and not clash_nodes and not any(protocol_links.values()):
        print("No supported nodes were parsed; preserving existing feeds.", file=sys.stderr)
        return 1

    OUTPUT.mkdir(parents=True, exist_ok=True)
    for feed, values in protocol_links.items():
        (OUTPUT / f"{feed}.txt").write_text(base64.b64encode("\n".join(values).encode()).decode() + "\n", encoding="ascii")
    (OUTPUT / "v2ray.txt").write_text(base64.b64encode("\n".join(v2ray).encode()).decode() + "\n", encoding="ascii")
    (OUTPUT / "ss-ssr.txt").write_text(base64.b64encode("\n".join(ss_ssr).encode()).decode() + "\n", encoding="ascii")
    document = {"port": 7890, "socks-port": 7891, "allow-lan": False, "mode": "rule", "log-level": "warning",
                "proxies": clash_nodes,
                "proxy-groups": [{"name": "AUTO", "type": "url-test", "proxies": [p["name"] for p in clash_nodes],
                                  "url": "https://www.gstatic.com/generate_204", "interval": 300}],
                "rules": ["MATCH,AUTO"]}
    (OUTPUT / "clash.yaml").write_text(yaml.safe_dump(document, allow_unicode=True, sort_keys=False), encoding="utf-8")
    protocol_links["v2ray"] = v2ray
    protocol_links["ss-ssr"] = ss_ssr
    protocol_links.pop("clash", None)
    update_readme_node_lists(protocol_links, clash_nodes)
    counts = ", ".join(f"{key}={len(values)}" for key, values in protocol_links.items())
    print(f"Published fastest nodes: {counts}, Clash={len(clash_nodes)} (maximum 30 per feed).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

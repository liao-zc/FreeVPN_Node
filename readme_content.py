"""Render the short Chinese subscription guide with stable primary and backup links."""

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent
BASE = "https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions"
CDN = "https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions"
FEEDS = (
    ("精选综合订阅（多协议）", "selected.txt"),
    ("V2Ray（VMess / VLESS / Trojan）", "v2ray.txt"),
    ("SS / SSR", "ss-ssr.txt"),
    ("Clash / Mihomo", "clash.yaml"),
    ("VMess", "vmess.txt"),
    ("VLESS", "vless.txt"),
    ("Shadowsocks", "ss.txt"),
    ("ShadowsocksR", "ssr.txt"),
    ("SOCKS", "socks.txt"),
    ("HTTP", "http.txt"),
    ("Trojan", "trojan.txt"),
    ("WireGuard", "wireguard.txt"),
    ("Hysteria2", "hysteria2.txt"),
)


def write_readme(protocol_links: dict[str, list[str]], clash_nodes: list[dict]) -> None:
    lines = [
        "# 免费节点订阅",
        "",
        "GitHub Actions 每 10 分钟自动搜索和更新公开节点。精选订阅通过 Mihomo 建立各节点隧道并下载测试文件，按实测下载速度从高到低排序，每个订阅分组最多保留 30 个节点。",
        "",
        "## 精选订阅",
        "",
        "主地址：",
    ]
    lines.extend(f"- {name}：{BASE}/{path}" for name, path in FEEDS)
    lines.extend(["", "备用地址："])
    lines.extend(f"- {name}：{CDN}/{path}" for name, path in FEEDS)
    lines.extend([
        "",
        "## 全量订阅",
        "",
        "全量地址包含本轮采集到且格式有效的多协议节点，不在 README 展开节点列表。客户端需要支持对应协议。",
        "",
        "主地址：",
        f"- 全量多协议订阅：{BASE}/all.txt",
        "",
        "备用地址：",
        f"- 全量多协议订阅：{CDN}/all.txt",
        "",
        "## 当前精选节点",
        "",
        "以下为隧道实测后的精选结果；全量订阅节点不在此列出。",
        "",
        "### V2Ray（VMess / VLESS / Trojan）",
        "```text",
        "\n".join(protocol_links.get("v2ray", [])) or "（本轮没有通过测速的节点）",
        "```",
        "",
        "### SS / SSR",
        "```text",
        "\n".join(protocol_links.get("ss-ssr", [])) or "（本轮没有通过测速的节点）",
        "```",
        "",
        "### Clash / Mihomo",
        "```yaml",
        yaml.safe_dump({"proxies": clash_nodes}, allow_unicode=True, sort_keys=False).rstrip() if clash_nodes else "proxies: []",
        "```",
        "",
    ])
    (ROOT / "README.md").write_text("\n".join(lines), encoding="utf-8")
"""Render the Chinese subscription guide and four comprehensive QR codes."""
from datetime import datetime, timezone
from pathlib import Path
import qrcode
import yaml

ROOT = Path(__file__).resolve().parent
BASE = "https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions"
CDN = "https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions"
FEEDS = (
    ("精选综合订阅（多协议）", "selected.txt"),
    ("V2Ray（VMess / VLESS / Trojan）", "v2ray.txt"),
    ("SSR（Shadowsocks + ShadowsocksR）", "ssr.txt"),
    ("SS / SSR（旧订阅地址兼容）", "ss-ssr.txt"),
    ("Clash / Mihomo", "clash.yaml"),
    ("VMess", "vmess.txt"), ("VLESS", "vless.txt"),
    ("Shadowsocks", "ss.txt"), ("SOCKS", "socks.txt"),
    ("HTTP", "http.txt"), ("Trojan", "trojan.txt"),
    ("WireGuard", "wireguard.txt"), ("Hysteria2", "hysteria2.txt"),
    ("非精选全量（多协议）", "all.txt"),
)
QR_FEEDS = {"selected.txt", "all.txt"}


def make_qr(url: str, path: Path) -> None:
    image = qrcode.make(url, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=5, border=3)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def write_readme(protocol_links: dict[str, list[str]], clash_nodes: list[dict]) -> None:
    qr_dir = ROOT / "qrcodes"
    qr_dir.mkdir(parents=True, exist_ok=True)
    for old_qr in qr_dir.glob("*.png"):
        old_qr.unlink()
    lines = [
        "# 免费节点订阅", "",
        "GitHub Actions 每 5 分钟尝试刷新节点；实际触发时间受 GitHub 调度影响。",
        f"最近成功刷新时间：{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        "精选节点按下载速度排序，境外测速不能代表实测可用性；每个订阅组最多 30 个，免费节点可能随时失效。",
        "", "## 精选订阅", "", "主订阅地址（每条单独一行）：", "",
    ]
    for label, path in FEEDS:
        url = f"{BASE}/{path}"
        lines.extend([f"### {label}", "", url])
        if path in QR_FEEDS:
            filename = f"main-{Path(path).stem}.png"
            make_qr(url, qr_dir / filename)
            lines.extend(["", f"![{label}主订阅二维码](qrcodes/{filename})"])
        lines.append("")
    lines.extend(["## 备用订阅", ""])
    for label, path in FEEDS:
        url = f"{CDN}/{path}"
        lines.extend([f"### {label}", "", url])
        if path in QR_FEEDS:
            filename = f"backup-{Path(path).stem}.png"
            make_qr(url, qr_dir / filename)
            lines.extend(["", f"![{label}备用订阅二维码](qrcodes/{filename})"])
        lines.append("")
    lines.extend([
        "## 当前精选节点", "",
        "### V2Ray（VMess / VLESS / Trojan）", "", "```text",
        "\n".join(protocol_links.get("v2ray", [])) or "（本轮没有通过隧道下载测试的节点）", "```",
        "", "### SSR（Shadowsocks + ShadowsocksR）", "", "```text",
        "\n".join(protocol_links.get("ssr", [])) or "（本轮没有通过隧道下载测试的节点）", "```",
        "", "### Clash / Mihomo", "", "```yaml",
        yaml.safe_dump({"proxies": clash_nodes}, allow_unicode=True, sort_keys=False).rstrip() if clash_nodes else "proxies: []",
        "```", "",
    ])
    (ROOT / "README.md").write_text("\n".join(lines), encoding="utf-8")

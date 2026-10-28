"""Render the Chinese subscription guide and QR codes for every stable feed URL."""
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
    ("Clash / Mihomo", "clash.yaml"),
    ("VMess", "vmess.txt"), ("VLESS", "vless.txt"),
    ("Shadowsocks", "ss.txt"), ("SOCKS", "socks.txt"),
    ("HTTP", "http.txt"), ("Trojan", "trojan.txt"),
    ("WireGuard", "wireguard.txt"), ("Hysteria2", "hysteria2.txt"),
    ("非精选全量（多协议）", "all.txt"),
)


def make_qr(url: str, path: Path) -> None:
    image = qrcode.make(url, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=5, border=3)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def write_readme(protocol_links: dict[str, list[str]], clash_nodes: list[dict]) -> None:
    qr_dir = ROOT / "qrcodes"
    lines = [
        "# 免费节点订阅", "",
        "GitHub Actions 每 10 分钟自动更新节点。精选节点须通过 GitHub Actions 境外运行环境中的 Mihomo 隧道下载测速，按下载速度排序，每个订阅组最多 30 个。境外测速不能代表上海移动 5G 的实测可用性；免费节点可能随时失效。",
        "", "## 精选订阅", "", "主订阅地址（每条单独一行）：", "",
    ]
    for label, path in FEEDS:
        url = f"{BASE}/{path}"
        qr_path = f"qrcodes/main-{Path(path).stem}.png"
        make_qr(url, qr_dir / f"main-{Path(path).stem}.png")
        lines.extend([f"### {label}", "", url, "", f"![{label}主订阅二维码]({qr_path})", ""])
    lines.extend(["## 备用订阅", "", "每条备用地址单独一行：", ""])
    for label, path in FEEDS:
        url = f"{CDN}/{path}"
        qr_path = f"qrcodes/backup-{Path(path).stem}.png"
        make_qr(url, qr_dir / f"backup-{Path(path).stem}.png")
        lines.extend([f"### {label}", "", url, "", f"![{label}备用订阅二维码]({qr_path})", ""])
    lines.extend([
        "## 节点说明", "",
        "V2Ray 订阅合并 VMess、VLESS 和 Trojan；SSR 订阅合并 Shadowsocks 与 ShadowsocksR。采集时按协议分别解析，再合并输出。Clash 订阅为 Mihomo 格式。",
        "非精选全量订阅包含本轮采集并成功解析的全部节点，不经过隧道下载测速筛选，数量较多且可用性未经验证。",
        "", "## 当前精选节点", "",
        "以下节点来自最近一次成功生成。排序依据是 GitHub Actions 环境经代理隧道下载测试的吞吐量。",
        "", "### V2Ray（VMess / VLESS / Trojan）", "", "```text",
        "\n".join(protocol_links.get("v2ray", [])) or "（本轮没有通过隧道下载测试的节点）", "```",
        "", "### SSR（Shadowsocks + ShadowsocksR）", "", "```text",
        "\n".join(protocol_links.get("ssr", [])) or "（本轮没有通过隧道下载测试的节点）", "```",
        "", "### Clash / Mihomo", "", "```yaml",
        yaml.safe_dump({"proxies": clash_nodes}, allow_unicode=True, sort_keys=False).rstrip() if clash_nodes else "proxies: []",
        "```", "",
    ])
    (ROOT / "README.md").write_text("\n".join(lines), encoding="utf-8")

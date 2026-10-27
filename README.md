# FreeVPN_Node

用 GitHub Actions 每 10 分钟拉取公开订阅源，解析并去重节点，生成三种订阅文件：V2Ray 家族 URI、Clash/Mihomo YAML、SS/SSR URI。工作流会把发生变化的文件提交回当前仓库。

## 订阅文件

生成路径：

- `subscriptions/v2ray.txt`：VMess、VLESS、Trojan，Base64 编码的 URI 列表。
- `subscriptions/clash.yaml`：Clash/Mihomo 配置，包含解析到的 VMess、VLESS、Trojan、SS、SSR 节点。
- `subscriptions/ss-ssr.txt`：SS、SSR，Base64 编码的 URI 列表。

部署到自己的 GitHub 仓库后，可把仓库名代入下列 jsDelivr 地址，分别作为对应类型的订阅地址：

```text
https://cdn.jsdelivr.net/gh/OWNER/REPO@main/subscriptions/v2ray.txt
https://cdn.jsdelivr.net/gh/OWNER/REPO@main/subscriptions/clash.yaml
https://cdn.jsdelivr.net/gh/OWNER/REPO@main/subscriptions/ss-ssr.txt
```

大陆网络对 GitHub、jsDelivr 和各地运营商的访问情况会变化，无法仅靠仓库代码保证任何公共域名始终可达。若 jsDelivr 在你的网络不可用，需要把同一份生成文件同步到你确认可访问的自有域名/CDN，并把该域名用作订阅地址。

## 部署

1. 将本项目推送到自己的 GitHub 仓库，默认分支设为 `main`。
2. 在仓库 Settings → Actions → General 中允许 Actions 创建和批准 PR 以外的内容写入（`GITHUB_TOKEN` 的 `contents: write` 权限）。
3. 在 Actions 页面手动运行一次 `Update public subscriptions`，之后由 cron 每 10 分钟触发。
4. 用上面的仓库地址订阅生成文件。

GitHub Actions 的 cron 可能延迟，仓库长期无活动时 GitHub 也可能停用定时工作流。工作流仅在输出变化时提交，防止无意义提交。运行频率是“尝试每 10 分钟”，并非实时服务 SLA。

## 配置来源

在 `sources.txt` 中每行添加一个公开的纯文本或 Base64 订阅 URL。当前示例来自三个用户提到的仓库和 Pawdroid/Free-servers。若上游调整了路径，可替换 URL。采集器支持常见 V2Ray URI、SS/SSR URI 和 Clash YAML；其他格式会跳过。每个源单独失败不会阻止其他源更新；所有源都不可用或没有可解析节点时，程序以错误退出并保留上一轮输出。

可以通过 Actions Variables 设置 `FETCH_TIMEOUT`、`MAX_SOURCE_BYTES`、`SOURCES_FILE` 或 `OUTPUT_DIR`。`SOURCES_FILE` 和 `OUTPUT_DIR` 是运行环境中的文件路径。

## 实现原理与边界

常见公开节点聚合项目大体采用以下流程：从项目自身的每日/定时节点文件，或其他公开 GitHub、Telegram、订阅地址获取内容；必要时 Base64 解码；解析 VMess/VLESS/Trojan/SS/SSR URI 或 Clash 的 `proxies`；规范化字段并按节点参数去重；按客户端需要输出 Base64 URI 订阅或 Clash YAML；最后由 GitHub Actions 定时更新并提交静态文件。一部分项目会再做 TCP/代理连通性检测，但仅 TCP 可连不代表代理可正常转发，也不等于安全可信。

本项目实现了抓取、解码、格式解析、按节点配置去重和多格式输出。它不替节点做真实代理拨测，也不声称这些公共节点稳定、匿名或安全。公开节点运营者可能观察未加密流量和连接元数据；不要通过不可信节点传输敏感数据。输出端目前是 GitHub 仓库本身以及兼容的 jsDelivr 静态镜像地址。

## 最近一周的仓库调研

按 GitHub 相关关键词检索、优先查看星数较高且在 **2026-10-20 至 2026-10-27（UTC）** 有更新的节点采集、聚合或订阅仓库；排除只做客户端/协议内核/规则集的项目。以下 30 个仓库用于比较 README、公开订阅文件和工作流所展示的实现方式。GitHub 星数和更新状态会持续变化。

| 仓库 | Stars | 最近 push（UTC） | 公开实现侧重点 |
|---|---:|---|---|
| [Pawdroid/Free-servers](https://github.com/Pawdroid/Free-servers) | 19,658 | 2026-10-27 | 周期更新多类型节点与订阅文件 |
| [free-nodes/clashfree](https://github.com/free-nodes/clashfree) | 17,062 | 2026-10-27 | 发布 Clash YAML 节点订阅 |
| [free-nodes/v2rayfree](https://github.com/free-nodes/v2rayfree) | 14,562 | 2026-10-27 | 发布 Base64/V2Ray URI 订阅 |
| [chengaopan/AutoMergePublicNodes](https://github.com/chengaopan/AutoMergePublicNodes) | 8,279 | 2026-10-27 | 汇总多个公开文本源并合并节点 |
| [awesome-vpn/awesome-vpn](https://github.com/awesome-vpn/awesome-vpn) | 6,778 | 2026-10-27 | 多协议公开节点汇总和周期更新 |
| [VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy](https://github.com/VPN-Subcription-Links/ClashX-V2Ray-TopFreeProxy) | 5,666 | 2026-10-27 | Clash/V2Ray 订阅和节点介绍 |
| [Barabama/FreeNodes](https://github.com/Barabama/FreeNodes) | 3,325 | 2026-10-26 | 抓取并自动发布 V2Ray/Clash 节点 |
| [snakem982/proxypool](https://github.com/snakem982/proxypool) | 2,220 | 2026-10-27 | 多来源代理池聚合 |
| [Au1rxx/free-vpn-subscriptions](https://github.com/Au1rxx/free-vpn-subscriptions) | 1,044 | 2026-10-27 | Clash、sing-box、V2Ray 多格式订阅 |
| [mfuu/FreeProxies](https://github.com/mfuu/FreeProxies) | 930 | 2026-10-27 | 发布 Clash/V2Ray 免费代理配置 |
| [0xRadikal/Free-v2ray-Configs](https://github.com/0xRadikal/Free-v2ray-Configs) | 771 | 2026-10-27 | 高频更新多协议节点及订阅 |
| [zhuhaiuk/free-nodes](https://github.com/zhuhaiuk/free-nodes) | 379 | 2026-10-27 | 定时生成多客户端订阅 |
| [F0rc3Run/F0rc3Run](https://github.com/F0rc3Run/F0rc3Run) | 321 | 2026-10-27 | 用 V2rayCollector 聚合多协议节点 |
| [crashgfw/free-airport-nodes](https://github.com/crashgfw/free-airport-nodes) | 296 | 2026-10-27 | 发布 V2Ray、Trojan、SS 等订阅 |
| [jichangx/free-nodes](https://github.com/jichangx/free-nodes) | 206 | 2026-10-26 | 定时更新并输出多客户端格式 |
| [xyfqzy/free-nodes](https://github.com/xyfqzy/free-nodes) | 189 | 2026-10-26 | 输出 Base64 与 YAML 订阅 |
| [HakurouKen/free-node](https://github.com/HakurouKen/free-node) | 180 | 2026-10-27 | V2Ray 公共节点集合 |
| [junjun266/FreeProxyGo](https://github.com/junjun266/FreeProxyGo) | 163 | 2026-10-27 | 周期性维护多协议公共订阅 |
| [MahanKenway/Freedom-V2Ray](https://github.com/MahanKenway/Freedom-V2Ray) | 118 | 2026-10-27 | 定时采集 VLESS、VMess、Trojan 等配置 |
| [Re0XIAOPA/AutoScrapeFreeNodes](https://github.com/Re0XIAOPA/AutoScrapeFreeNodes) | 114 | 2026-10-26 | 自动抓取公开免费节点 |
| [wenxig/free-nodes-sub](https://github.com/wenxig/free-nodes-sub) | 106 | 2026-10-27 | 抓取 free-nodes 并转换多种订阅格式 |
| [VoroninaYanina/free-nodes](https://github.com/VoroninaYanina/free-nodes) | 103 | 2026-10-27 | V2Ray/SS/Trojan 公共节点订阅 |
| [vorz1k/v2box](https://github.com/vorz1k/v2box) | 99 | 2026-10-26 | 发布 V2Ray/VLESS/Trojan 订阅 |
| [mehdirzfx/v2ray-sub](https://github.com/mehdirzfx/v2ray-sub) | 75 | 2026-10-23 | 合并多类型 V2Ray 订阅链接 |
| [Thordata/awesome-free-proxy-list](https://github.com/Thordata/awesome-free-proxy-list) | 58 | 2026-10-27 | 验证节点后发布列表与订阅 |
| [skka3134/Free-servers](https://github.com/skka3134/Free-servers) | 41 | 2026-10-27 | 周期性发布多类型节点订阅 |
| [morpheusadam/v2ray-config](https://github.com/morpheusadam/v2ray-config) | 38 | 2026-10-26 | 拉取、解码并拨测后生成订阅 |
| [Alirewa/V2ray-Configs](https://github.com/Alirewa/V2ray-Configs) | 31 | 2026-10-27 | 从公开频道和 GitHub 源采集配置 |
| [freenodess/freenodess](https://github.com/freenodess/freenodess) | 20 | 2026-10-27 | 多地区、多客户端订阅输出 |
| [yuluo688/clash-hot-countries](https://github.com/yuluo688/clash-hot-countries) | 0 | 2026-10-26 | 定时生成按地区分类的 Clash 订阅 |

调研结论是，项目间主要差别在于上游入口、节点筛选强度和发布格式；聚合、Base64 解码、协议解析、去重、生成静态订阅和定时提交是常见共性。本项目沿用这条通用链路，并把来源放在可编辑清单中。订阅源内容及可用性由上游控制，使用前应自行检查来源。

# 免费节点订阅

GitHub Actions 每 10 分钟自动搜索和更新公开节点。精选订阅通过 Mihomo 建立各节点隧道并下载测试文件，按实测下载速度从高到低排序，每个订阅分组最多保留 30 个节点。

## 精选订阅

主地址：
- 精选综合订阅（多协议）：https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/selected.txt
- V2Ray（VMess / VLESS / Trojan）：https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/v2ray.txt
- SS / SSR：https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/ss-ssr.txt
- Clash / Mihomo：https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/clash.yaml
- VMess：https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/vmess.txt
- VLESS：https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/vless.txt
- Shadowsocks：https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/ss.txt
- ShadowsocksR：https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/ssr.txt
- SOCKS：https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/socks.txt
- HTTP：https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/http.txt
- Trojan：https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/trojan.txt
- WireGuard：https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/wireguard.txt
- Hysteria2：https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/hysteria2.txt

备用地址：
- 精选综合订阅（多协议）：https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/selected.txt
- V2Ray（VMess / VLESS / Trojan）：https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/v2ray.txt
- SS / SSR：https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/ss-ssr.txt
- Clash / Mihomo：https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/clash.yaml
- VMess：https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/vmess.txt
- VLESS：https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/vless.txt
- Shadowsocks：https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/ss.txt
- ShadowsocksR：https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/ssr.txt
- SOCKS：https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/socks.txt
- HTTP：https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/http.txt
- Trojan：https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/trojan.txt
- WireGuard：https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/wireguard.txt
- Hysteria2：https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/hysteria2.txt

## 全量订阅

全量地址包含本轮采集到且格式有效的多协议节点，不在 README 展开节点列表。客户端需要支持对应协议。

主地址：
- 全量多协议订阅：https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/all.txt

备用地址：
- 全量多协议订阅：https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/all.txt

## 当前精选节点

以下为隧道实测后的精选结果；全量订阅节点不在此列出。

### V2Ray（VMess / VLESS / Trojan）
```text
vmess://eyJhZGQiOiIxMDQuMTcuMTQ3LjIyMiIsImFpZCI6IjAiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0Ijoidm1lc3MubGJ3NjY2LmRwZG5zLm9yZyIsImlkIjoiMGNmNmQ5NzAtM2YxZC00YWFlLWE5ODktOTJhOGY3NmFlM2RiIiwiaW5zZWN1cmUiOiIwIiwibmV0Ijoid3MiLCJwYXRoIjoiL3dzP2VkPTIwNDgiLCJwY3MiOiIiLCJwb3J0IjoiODAiLCJwcyI6IkBGYXJhelYycmF5ICIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiIiLCJ0eXBlIjoiLS0tIiwidiI6IjIiLCJ2Y24iOiIifQ
vmess://eyJhZGQiOiIxMDQuMTcuMTQ3LjIyMiIsImFpZCI6IjAiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0Ijoidm1lc3MubGJ3NjY2LmRwZG5zLm9yZyIsImlkIjoiMGNmNmQ5NzAtM2YxZC00YWFlLWE5ODktOTJhOGY3NmFlM2RiIiwiaW5zZWN1cmUiOiIwIiwibmV0Ijoid3MiLCJwYXRoIjoiL3dzP2VkPTIwNDgiLCJwY3MiOiIiLCJwb3J0IjoiODAiLCJwcyI6IkNBIFx1ZDgzY1x1ZGRlOFx1ZDgzY1x1ZGRlNiB8IEBSYXlkaWthbHggfCBGMjVDMzIiLCJzY3kiOiJhdXRvIiwic25pIjoiIiwidGxzIjoibm9uZSIsInR5cGUiOiItLS0iLCJ2IjoiMiIsInZjbiI6IiIsIm5hbWUiOiJDQSBcdWQ4M2NcdWRkZThcdWQ4M2NcdWRkZTYgfCBAUmF5ZGlrYWx4IHwgRjI1QzMyIn0
vmess://eyJhZGQiOiIxNzIuNjcuMTg3LjE0NSIsImFpZCI6IjAiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0Ijoidm1lc3MubGJ3NjY2LmRwZG5zLm9yZyIsImlkIjoiMGNmNmQ5NzAtM2YxZC00YWFlLWE5ODktOTJhOGY3NmFlM2RiIiwibmFtZSI6IkNBIFx1ZDgzY1x1ZGRlOFx1ZDgzY1x1ZGRlNiB8IEBSYXlkaWthbHggfCAwQUQ1MTkiLCJuZXQiOiJ3cyIsInBhdGgiOiIvd3M_ZWQ9MjA0OCIsInBvcnQiOiI4MCIsInBzIjoiQ0EgXHVkODNjXHVkZGU4XHVkODNjXHVkZGU2IHwgQFJheWRpa2FseCB8IDBBRDUxOSIsInNjeSI6ImF1dG8iLCJzbmkiOiIiLCJ0bHMiOiJub25lIiwidHlwZSI6Im5vbmUiLCJ2IjoiMiJ9
vmess://eyJ2IjoiMiIsInBzIjoiXHVkODNjXHVkZGZhXHVkODNjXHVkZGY4VVNfMzM0fDU5NUtCL3N8UzAwNC0yNjA2MTggW2JlNDRhOWI1ZDNiYl0iLCJhZGQiOiIxMDQuMTcuMTQ3LjIyMiIsInBvcnQiOiI4MCIsImlkIjoiMGNmNmQ5NzAtM2YxZC00YWFlLWE5ODktOTJhOGY3NmFlM2RiIiwiYWlkIjoiMCIsInNjeSI6ImF1dG8iLCJuZXQiOiJ3cyIsInR5cGUiOiJub25lIiwiaG9zdCI6InZtZXNzLmxidzY2Ni5kcGRucy5vcmciLCJwYXRoIjoiL3dzIiwidGxzIjoiIn0
vmess://eyJhZGQiOiIxMDQuMTcuMTQ3LjIyMiIsImFpZCI6MCwiaG9zdCI6InZtZXNzLmxidzY2Ni5kcGRucy5vcmciLCJpZCI6IjBjZjZkOTcwLTNmMWQtNGFhZS1hOTg5LTkyYThmNzZhZTNkYiIsIm5ldCI6IndzIiwicGF0aCI6Ii93cyIsInBvcnQiOiI4MCIsInBzIjoiQ0EgXHVkODNjXHVkZGU4XHVkODNjXHVkZGU2IHwgQFJheWRpa2FseCB8IEY2NUI5RCIsInNuaSI6InZtZXNzLmxidzY2Ni5kcGRucy5vcmciLCJ0bHMiOiIiLCJ0eXBlIjoibm9uZSIsInYiOiIyIn0
vmess://eyJ2IjoiMiIsInBzIjoiXHVkODNjXHVkZGZhXHVkODNjXHVkZGY4VVNfMzU1fDU2OUtCL3N8QTAwNC0yNjA2MTggW2M1MTc1ZmYwZGViZl0iLCJhZGQiOiIxNzIuNjcuMTg3LjE0NSIsInBvcnQiOiI4MCIsImlkIjoiMGNmNmQ5NzAtM2YxZC00YWFlLWE5ODktOTJhOGY3NmFlM2RiIiwiYWlkIjoiMCIsInNjeSI6ImF1dG8iLCJuZXQiOiJ3cyIsInR5cGUiOiJub25lIiwiaG9zdCI6InZtZXNzLmxidzY2Ni5kcGRucy5vcmciLCJwYXRoIjoiL3dzIiwidGxzIjoiIiwic25pIjoidm1lc3MubGJ3NjY2LmRwZG5zLm9yZyJ9
vmess://eyJhZGQiOiIxNzIuNjcuMTg3LjE0NSIsImFpZCI6MCwiaG9zdCI6InZtZXNzLmxidzY2Ni5kcGRucy5vcmciLCJpZCI6IjBjZjZkOTcwLTNmMWQtNGFhZS1hOTg5LTkyYThmNzZhZTNkYiIsIm5ldCI6IndzIiwicGF0aCI6Ii93cyIsInBvcnQiOiI4MCIsInBzIjoiQ0EgXHVkODNjXHVkZGU4XHVkODNjXHVkZGU2IHwgQFJheWRpa2FseCB8IEM0MDIzNSIsInNuaSI6IiIsInRscyI6IiIsInR5cGUiOiJub25lIiwidiI6IjIifQ
vless://4e4f1f70-5e56-4a76-bb9d-db087f4690c4@104.18.42.98:443?encryption=none&type=ws&security=tls&sni=jp3.yohototo.top&fp=chrome&path=%2Ftyxyws&host=jp3.yohototo.top#%F0%9F%87%AF%F0%9F%87%B5%5Bwww.v2nodes.com%5D%20vless-JP-1...%20%235
vless://4e4f1f70-5e56-4a76-bb9d-db087f4690c4@104.18.42.98:443?encryption=none&type=ws&security=tls&sni=jp3.yohototo.top&fp=chrome&path=%2Ftyxyws&host=jp3.yohototo.top#%F0%9F%87%AF%F0%9F%87%B5%5Bwww.v2nodes.com%5D%20vless-JP-1...%20%235%20%5Ba85de411b13d78e4%5D
vless://4e4f1f70-5e56-4a76-bb9d-db087f4690c4@104.18.42.98:443?encryption=none&type=ws&security=tls&sni=jp3.yohototo.top&fp=chrome&path=%2Ftyxyws&host=jp3.yohototo.top#%F0%9F%8F%B3%EF%B8%8F_%E6%9C%AA%E7%9F%A5_271%20%5Bee06d986b10877a1%5D
vless://4e4f1f70-5e56-4a76-bb9d-db087f4690c4@104.18.42.98:443?encryption=none&security=tls&type=ws&host=jp3.yohototo.top&path=%2Ftyxyws&sni=jp3.yohototo.top&fp=chrome#%F0%9F%8F%B3%EF%B8%8F_%E6%9C%AA%E7%9F%A5_271
vless://4e4f1f70-5e56-4a76-bb9d-db087f4690c4@104.18.42.98:443?host=jp3.yohototo.top&path=%2Ftyxyws&security=tls&sni=jp3.yohototo.top&type=ws#CA
```

### SS / SSR
```text
ss://cmM0LW1kNToxNGZGUHJiZXpFM0hEWnpzTU9yNg@138.199.42.68:8080#shadowsocks-1827147700
ss://cmM0LW1kNToxNGZGUHJiZXpFM0hEWnpzTU9yNg@138.199.42.68:8080#%F0%9F%87%BA%F0%9F%87%B8US_4%7C1.4MB%2Fs%20%5Bb3491eae71bd%5D
ss://cmM0LW1kNToxNGZGUHJiZXpFM0hEWnpzTU9yNg@138.199.42.68:8080#US
ssr://MTA3LjE1MS4xODIuMjUzOjgwODA6b3JpZ2luOnJjNC1tZDU6cGxhaW46TVRSbVJsQnlZbVY2UlROSVJGcDZjMDFQY2pZLz9yZW1hcmtzPVUxTlNMZWUtanVXYnZTMU9SdWluby1tVWdlaUhxdVdJdHVXSnB5MURhR0YwUjFCVUxWUnBhMVJ2YXkxWmIzVlVkV0psTFRFd055NHhOVEV1TVRneUxqSTFNem80TURnd0lGczBZVGMxTWpFeU5tRTNPVFkyTVRkbFhR
ssr://YXBpLm1laXR1YW44OC5jb206MzkyNjY6YXV0aF9hZXMxMjhfbWQ1OnJjNC1tZDU6cGxhaW46WkdreE5WQlcvP29iZnNwYXJhbT1aamRrTWpNNU1qa3VaRzkxZVdsdUxtTnZiUSZwcm90b3BhcmFtPU1qTTVNams2TlRZek5UTTNNRE15JnJlbWFya3M9OEotSHV2Q2ZoN2hWVTE4ME5UQjhOVGcwUzBJdmMzeFNNREF5TFRJMk1EWXhPQ0JiWXpoak1qQTJPREZsTURGaFhR
ssr://YXBpLm1laXR1YW44OC5jb206NDQ4ODM6YXV0aF9hZXMxMjhfbWQ1OmNoYWNoYTIwLWlldGY6dGxzMS4yX3RpY2tldF9hdXRoOlpHa3hOVkJXLz9vYmZzcGFyYW09Tm1ZMU1qRTROVEl5TG1SdmRYbHBiaTVqYjIwJnByb3RvcGFyYW09TWpFNE5USXlPakJvWmtOS2F3JnJlbWFya3M9OEotSHV2Q2ZoN2hWVTE4ME9USjhOVEV4UzBJdmMzeFNNREF5TFRJMk1EWXhPQ0JiT0RjeVpEa3hOelJoWmpoaVhR
ssr://YXBpLm1laXR1YW44OC5jb206Mjc1NjE6YXV0aF9hZXMxMjhfbWQ1OnJjNC1tZDU6cGxhaW46WkdreE5WQlcvP29iZnNwYXJhbT1ObVkxTWpFNE5USXlMbVJ2ZFhscGJpNWpiMjAmcHJvdG9wYXJhbT1NakU0TlRJeU9qQm9aa05LYXcmcmVtYXJrcz04Si1IdXZDZmg3aFZVMTgwT1RGOE5qRTBTMEl2YzN4U01EQXlMVEkyTURZeE9DQmJOamd5WkdVNU1EUTNNR05oWFE
ssr://YXBpLm1laXR1YW44OC5jb206Mjk3OTA6YXV0aF9hZXMxMjhfbWQ1OmNoYWNoYTIwLWlldGY6dGxzMS4yX3RpY2tldF9hdXRoOlpHa3hOVkJXLz9vYmZzcGFyYW09Wmpka01qTTVNamt1Wkc5MWVXbHVMbU52YlEmcHJvdG9wYXJhbT1Nak01TWprNk5UWXpOVE0zTURNeSZyZW1hcmtzPThKLUh1dkNmaDdoVlUxODBOVEY4TXpnNFMwSXZjM3hTTURBeUxUSTJNRFl4T0NCYk9EZ3labUprTVRZMk5qQmlYUQ
ssr://YXBpLm1laXR1YW44OC5jb206NjE1NTg6YXV0aF9hZXMxMjhfbWQ1OnJjNC1tZDU6dGxzMS4yX3RpY2tldF9hdXRoOlpHa3hOVkJXLz9vYmZzcGFyYW09Tm1ZMU1qRTROVEl5TG1SdmRYbHBiaTVqYjIwJnByb3RvcGFyYW09TWpFNE5USXlPakJvWmtOS2F3JnJlbWFya3M9OEotSHV2Q2ZoN2hWVTE4ME9UWjhORFk0UzBJdmMzeFNNREF5TFRJMk1EWXhPQ0JiTTJNeU9ESmlZalZqWldGbFhR
ssr://YXBpLm1laXR1YW44OC5jb206MjkzOTI6YXV0aF9hZXMxMjhfbWQ1OnJjNC1tZDU6dGxzMS4yX3RpY2tldF9hdXRoOlpHa3hOVkJXLz9vYmZzcGFyYW09Tm1ZMU1qRTROVEl5TG1SdmRYbHBiaTVqYjIwJnByb3RvcGFyYW09TWpFNE5USXlPakJvWmtOS2F3JnJlbWFya3M9OEotSHV2Q2ZoN2hWVTE4ME9UUjhORFl3UzBJdmMzeFNNREF5TFRJMk1EWXhPQ0JiTW1Kak4ySTJabU5qTW1JMFhR
```

### Clash / Mihomo
```yaml
proxies:
- name: 🇫🇷FR_47|7.5MB/s|R002-260618 [39873ef4d996]
  port: 443
  server: 172.64.68.89
  skip-cert-verify: true
  sub_tag: R002-260618
  tls: true
  type: http
  udp: true
- name: '@FarazV2ray '
  type: vmess
  server: 104.17.147.222
  port: 80
  uuid: 0cf6d970-3f1d-4aae-a989-92a8f76ae3db
  alterId: 0
  cipher: auto
  udp: true
  tls: false
  network: ws
  ws-opts:
    path: /ws?ed=2048
    headers:
      Host: vmess.lbw666.dpdns.org
- name: برای اتصال دائمی جوین شو🔐 TelegramID ⌲Express_freevpn 🪩
  type: wireguard
  server: 162.159.192.2
  port: 500
  private-key: +AYnqJYinZIJ6yZwIjmirctmPqzfctf6H2fTqywa/XM=
  public-key: bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=
  ip: 172.16.0.2/32
  udp: true
  reserved:
  - 39
  - 4
  - 107
  mtu: 1280
- name: CA 🇨🇦 | @Raydikalx | 0AD519
  type: vmess
  server: 172.67.187.145
  port: 80
  uuid: 0cf6d970-3f1d-4aae-a989-92a8f76ae3db
  alterId: 0
  cipher: auto
  udp: true
  tls: false
  network: ws
  ws-opts:
    path: /ws?ed=2048
    headers:
      Host: vmess.lbw666.dpdns.org
- name: us|81c2|puddincat07@Telegram
  password: 4291c983-c520-46ac-82cc-48f14bef573f
  port: 35013
  server: 129.213.91.185
  skip-cert-verify: true
  sni: 129.213.91.185
  tls: false
  type: hysteria2
- name: 🇺🇸US_334|595KB/s|S004-260618 [be44a9b5d3bb]
  type: vmess
  server: 104.17.147.222
  port: 80
  uuid: 0cf6d970-3f1d-4aae-a989-92a8f76ae3db
  alterId: 0
  cipher: auto
  udp: true
  tls: false
  network: ws
  ws-opts:
    path: /ws
    headers:
      Host: vmess.lbw666.dpdns.org
- cipher: rc4-md5
  name: shadowsocks-1827147700
  password: 14fFPrbezE3HDZzsMOr6
  port: 8080
  server: 138.199.42.68
  type: ss
  udp: true
- cipher: rc4-md5
  obfs: plain
  password: 14fFPrbezE3HDZzsMOr6
  port: 8080
  protocol: origin
  server: 107.151.182.253
  type: ssr
  name: SSR-美国-NF解锁自制剧-ChatGPT-TikTok-YouTube-107.151.182.253:8080 [4a752126a796617e]
- name: برای اتصال دائمی جوین شو🔐 TelegramID ⌲Express_freevpn 🪩-2
  type: wireguard
  server: 162.159.192.3
  port: 500
  private-key: 2D+QMolgGWVRVGdJJvsQ4VBDCcZTym0c1sFN00PeMUs=
  public-key: bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=
  ip: 172.16.0.2/32
  udp: true
  reserved:
  - 213
  - 74
  - 19
  mtu: 1280
- name: hysteria2-1853974956
  password: bce6c821-200d-421f-bf3d-7159e5246ea0
  port: 33333
  server: 155.248.209.237
  skip-cert-verify: true
  sni: hy2.123266.xyz
  type: hysteria2
- name: hysteria2-1832863516
  password: bce6c821-200d-421f-bf3d-7159e5246ea0
  port: 33333
  server: 155.248.209.237
  skip-cert-verify: true
  sni: ''
  type: hysteria2
- name: hysteria2-1832764823
  password: gf1:gfhysteria2024
  port: 443
  server: 66.94.121.46
  skip-cert-verify: true
  sni: www.broadcom.com
  type: hysteria2
- name: 🇺🇸US_450|584KB/s|R002-260618 [c8c20681e01a]
  type: ssr
  server: api.meituan88.com
  port: 39266
  cipher: rc4-md5
  password: di15PV
  protocol: auth_aes128_md5
  obfs: plain
  obfs-param: f7d23929.douyin.com
  protocol-param: 23929:563537032
- name: 🇺🇸US_492|511KB/s|R002-260618 [872d9174af8b]
  type: ssr
  server: api.meituan88.com
  port: 44883
  cipher: chacha20-ietf
  password: di15PV
  protocol: auth_aes128_md5
  obfs: tls1.2_ticket_auth
  obfs-param: 6f5218522.douyin.com
  protocol-param: 218522:0hfCJk
- name: hysteria2-1908512041
  password: dd50a499-7e43-4589-8490-f3b9c2451473
  port: 443
  server: 109.235.49.234
  skip-cert-verify: true
  sni: nl-hy-test.tcp-reset-club.net
  type: hysteria2
- name: hysteria2-1923902590
  password: 529f1911-04d5-4427-94b9-c851fd459a27
  port: 443
  server: 109.235.49.234
  skip-cert-verify: false
  sni: nl-hy-test.tcp-reset-club.net
  type: hysteria2
- name: 🇺🇸US_492|511KB/s|R002-260618 [872d9174af8b]-2
  cipher: chacha20-ietf
  obfs: tls1.2_ticket_auth
  obfs-param: 6f5218522.douyin.com
  password: di15PV
  port: 44883
  protocol: auth_aes128_md5
  protocol-param: 218522:0hfCJk
  server: api.meituan88.com
  sub_tag: R002-260618
  type: ssr
  udp: true
- name: 🇳🇱NL_255|505KB/s|R002-260618 [8b79f7273e58]
  cipher: chacha20-ietf
  obfs: tls1.2_ticket_auth
  password: dongtaiwang.com
  port: 33336
  protocol: auth_chain_a
  server: 109.104.153.43
  sub_tag: R002-260618
  type: ssr
  udp: true
- name: hysteria2-1832764816
  password: 96ab5cd282733fd4c312a61f972f330a
  port: 443
  server: 45.32.10.7
  skip-cert-verify: false
  sni: vp3.yysyy.online
  type: hysteria2
- name: hysteria2-1832764952
  type: hysteria2
  server: vp3.yysyy.online
  port: 443
  password: 96ab5cd282733fd4c312a61f972f330a
  udp: true
  sni: vp3.yysyy.online
- name: hysteria2-1832765307
  password: b4c8ee9caa74b7ba0a61
  port: 35076
  server: 78.17.128.153
  skip-cert-verify: true
  sni: scrap.halyvanedorogo.ru
  type: hysteria2
- name: 🇺🇸US_355|569KB/s|A004-260618 [c5175ff0debf]
  alterId: 0
  cipher: auto
  network: ws
  port: 80
  server: 172.67.187.145
  skip-cert-verify: false
  sub_tag: A004-260618
  tls: false
  type: vmess
  udp: true
  uuid: 0cf6d970-3f1d-4aae-a989-92a8f76ae3db
  ws-opts:
    headers:
      Host: vmess.lbw666.dpdns.org
    path: /ws
  xudp: true
  packet-encoding: xudp
  servername: vmess.lbw666.dpdns.org
- name: 🇺🇸US_355|569KB/s|A004-260618 [c5175ff0debf]-2
  type: vmess
  server: 172.67.187.145
  port: 80
  uuid: 0cf6d970-3f1d-4aae-a989-92a8f76ae3db
  alterId: 0
  cipher: auto
  udp: true
  tls: false
  network: ws
  ws-opts:
    path: /ws
    headers:
      Host: vmess.lbw666.dpdns.org
- name: hysteria2-1832765048
  password: b4c8ee9caa74b7ba0a61
  port: 35076
  server: scrap.halyvanedorogo.ru
  skip-cert-verify: true
  sni: scrap.halyvanedorogo.ru
  type: hysteria2
- name: 🇺🇸US_334|595KB/s|S004-260618 [be44a9b5d3bb]-2
  alpn:
  - ''
  alterId: '0'
  cipher: auto
  network: ws
  port: 80
  server: 104.17.147.222
  skip-cert-verify: false
  sub_tag: S004-260618
  tls: false
  type: vmess
  udp: true
  uuid: 0cf6d970-3f1d-4aae-a989-92a8f76ae3db
  ws-opts:
    early-data-header-name: Sec-WebSocket-Protocol
    headers:
      Host: vmess.lbw666.dpdns.org
    max-early-data: 2048
    path: /ws
  xudp: true
  packet-encoding: xudp
- name: 🇺🇸US_450|584KB/s|R002-260618 [c8c20681e01a]-2
  cipher: rc4-md5
  obfs: plain
  obfs-param: f7d23929.douyin.com
  password: di15PV
  port: 39266
  protocol: auth_aes128_md5
  protocol-param: 23929:563537032
  server: api.meituan88.com
  sub_tag: R002-260618
  type: ssr
  udp: true
- name: hysteria2-1828371338
  password: H7mP2xY9kJ4nQ8wR5tF6vB3z
  port: 443
  server: 103.115.109.49
  skip-cert-verify: true
  sni: https://t.me/wangcai2
  type: hysteria2
- name: hysteria2-1830466990
  password: H7mP2xY9kJ4nQ8wR5tF6vB3z
  port: 443
  server: 103.115.109.49
  skip-cert-verify: true
  sni: https%3a%2f%2ft.me%2fwangcai2%f0%9f%87%a8%f0%9f%87%b3
  type: hysteria2
- name: hysteria2-1874927573
  password: H7mP2xY9kJ4nQ8wR5tF6vB3z
  port: 443
  server: 202.146.222.29
  skip-cert-verify: true
  sni: https://t.me/wangcai2üá®üá
  type: hysteria2
- name: hysteria2-1853331603
  password: H7mP2xY9kJ4nQ8wR5tF6vB3z
  port: 443
  server: 202.146.222.29
  skip-cert-verify: true
  sni: https://t.me/wangcai2ⁿß«ⁿß
  type: hysteria2
```

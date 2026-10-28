# 免费节点订阅

GitHub Actions 每 10 分钟自动更新节点。精选节点须通过 GitHub Actions 境外运行环境中的 Mihomo 隧道下载测速，按下载速度排序，每个订阅组最多 30 个。境外测速不能代表上海移动 5G 的实测可用性；免费节点可能随时失效。

## 精选订阅

主订阅地址（每条单独一行）：

### 精选综合订阅（多协议）

https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/selected.txt

### V2Ray（VMess / VLESS / Trojan）

https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/v2ray.txt

### SSR（Shadowsocks + ShadowsocksR）

https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/ssr.txt

### SS / SSR（旧订阅地址兼容）

https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/ss-ssr.txt

### Clash / Mihomo

https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/clash.yaml

### VMess

https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/vmess.txt

### VLESS

https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/vless.txt

### Shadowsocks

https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/ss.txt

### SOCKS

https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/socks.txt

### HTTP

https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/http.txt

### Trojan

https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/trojan.txt

### WireGuard

https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/wireguard.txt

### Hysteria2

https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/hysteria2.txt

### 非精选全量（多协议）

https://raw.githubusercontent.com/liao-zc/FreeVPN_Node/main/subscriptions/all.txt

## 备用订阅

每条备用地址单独一行：

### 精选综合订阅（多协议）

https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/selected.txt

### V2Ray（VMess / VLESS / Trojan）

https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/v2ray.txt

### SSR（Shadowsocks + ShadowsocksR）

https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/ssr.txt

### SS / SSR（旧订阅地址兼容）

https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/ss-ssr.txt

### Clash / Mihomo

https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/clash.yaml

### VMess

https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/vmess.txt

### VLESS

https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/vless.txt

### Shadowsocks

https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/ss.txt

### SOCKS

https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/socks.txt

### HTTP

https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/http.txt

### Trojan

https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/trojan.txt

### WireGuard

https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/wireguard.txt

### Hysteria2

https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/hysteria2.txt

### 非精选全量（多协议）

https://cdn.jsdelivr.net/gh/liao-zc/FreeVPN_Node@main/subscriptions/all.txt

## 综合订阅二维码

以下四张二维码对应精选与全量订阅的主、备用地址。

### 精选主订阅

![精选主订阅](qrcodes/main-selected.png)

### 精选备用订阅

![精选备用订阅](qrcodes/backup-selected.png)

### 全量主订阅

![全量主订阅](qrcodes/main-all.png)

### 全量备用订阅

![全量备用订阅](qrcodes/backup-all.png)

## 节点说明

V2Ray 订阅合并 VMess、VLESS 和 Trojan；SSR 订阅合并 Shadowsocks 与 ShadowsocksR。采集时按协议分别解析，再合并输出。Clash 订阅为 Mihomo 格式。
非精选全量订阅包含本轮采集并成功解析的全部节点，不经过隧道下载测速筛选，数量较多且可用性未经验证。

## 当前精选节点

以下节点来自最近一次成功生成。排序依据是 GitHub Actions 环境经代理隧道下载测试的吞吐量。

### V2Ray（VMess / VLESS / Trojan）

```text
vless://2bcfbfba-b446-4ad5-93ad-72af9e008f61@172.67.174.10:443?encryption=none&security=tls&sni=blackshadow.dpdns.org&fp=chrome&type=ws&host=blackshadow.dpdns.org&path=%2F44.209.52.7-443#CA
vless://d342d11e-d424-4583-b36e-524ab1f0afa4@188.114.97.3:2083?encryption=none&type=ws&security=tls&sni=newwk1.f1w.de5.net&fp=chrome&path=%2F&host=newwk1.f1w.de5.net#%F0%9F%87%AB%F0%9F%87%B7FR_249%7C703KB%2Fs%7CB007-260618%20%5B4de2ae3b13a9%5D
vless://79575802-3af5-4212-acde-8dd18ee668ea@199.232.78.159:80?encryption=none&host=rb24.ir&path=ws/?ed=2048/@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1@VPNine1/?2048&security=none&type=ws#US
vless://79575802-3af5-4212-acde-8dd18ee668ea@199.232.78.159:80?path=ws/?ed=2048/@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr@vpnserverrr/?2048&security=none&encryption=none&host=rb24.ir&type=ws#US
vmess://eyJhZGQiOiIxNzIuNjQuODAuMSIsImFpZCI6IjAiLCJob3N0IjoidjJyYXkxLmRvemFwcC54eXoiLCJpZCI6IjYwNDQxNTQ4LWI2OGUtNDNiMi04MTkxLWUzYjg4NGJlNGIzYyIsIm5ldCI6IndzIiwicGF0aCI6Ii9sTW5zWlVONC8iLCJwb3J0IjoiODQ0MyIsInBzIjoiQ0EgXHVkODNjXHVkZGU4XHVkODNjXHVkZGU2IHwgQFJheWRpa2FseCB8IEM2NTk3NCIsInNlY3VyaXR5IjoiYXV0byIsInNraXAtY2VydC12ZXJpZnkiOnRydWUsInNuaSI6IiIsInRscyI6InRscyIsInR5cGUiOiJhdXRvIiwidiI6IjIiLCJzY3kiOiJhdXRvIiwiYWxwbiI6IiIsImZwIjoiIn0
vmess://eyJ2IjoiMiIsInBzIjoiXHVkODNjXHVkZGVmXHVkODNjXHVkZGY1SlBfNDl8MjExS0Ivc3xNMDAyLTI2MDYxOCBbMmUzZGRjMzJjMDY1XSIsImFkZCI6IjE2Mi4xNTkuMTMwLjIzNCIsInBvcnQiOiIyMDgzIiwiaWQiOiJhYzI1MTIzNy01NzZmLTQwYzgtYTU0My01NTQ5NjBjOTU4YjEiLCJhaWQiOiIwIiwic2N5IjoiYXV0byIsIm5ldCI6IndzIiwidHlwZSI6Im5vbmUiLCJob3N0Ijoib3IzLnNmYWNnLnVrIiwicGF0aCI6Ii9vcjMiLCJ0bHMiOiJ0bHMiLCJzbmkiOiJvcjMuc2ZhY2cudWsifQ
vmess://eyJhZGQiOiIxNjIuMTU5LjEzMC4yMzQiLCJhaWQiOjAsImhvc3QiOiJvcjMuc2ZhY2cudWsiLCJpZCI6ImFjMjUxMjM3LTU3NmYtNDBjOC1hNTQzLTU1NDk2MGM5NThiMSIsIm5ldCI6IndzIiwicGF0aCI6Ii9vcjMiLCJwb3J0IjoiMjA4MyIsInBzIjoiQ0EgXHVkODNjXHVkZGU4XHVkODNjXHVkZGU2IHwgQFJheWRpa2FseCB8IDIwMUY4OCIsInNuaSI6Im9yMy5zZmFjZy51ayIsInRscyI6InRscyIsInR5cGUiOiJub25lIiwidiI6IjIifQ
vmess://eyJ2IjoiMiIsInBzIjoiXHVkODNjXHVkZGZhXHVkODNjXHVkZGY4VVNfMzgwfDMxMktCL3N8TTAwMy0yNjA4MDYgWzRiYjZhZmQwNWNiZF0iLCJhZGQiOiIxNzIuNjQuODAuMSIsInBvcnQiOiI4NDQzIiwiaWQiOiI2MDQ0MTU0OC1iNjhlLTQzYjItODE5MS1lM2I4ODRiZTRiM2MiLCJhaWQiOiIwIiwic2N5IjoiYXV0byIsIm5ldCI6IndzIiwidHlwZSI6Im5vbmUiLCJob3N0IjoidjJyYXkxLmRvemFwcC54eXoiLCJwYXRoIjoiL2xNbnNaVU40LyIsInRscyI6InRscyIsInNuaSI6InYycmF5MS5kb3phcHAueHl6In0
vmess://eyJ2IjoiMiIsInBzIjoiQ0EgXHVkODNjXHVkZGU4XHVkODNjXHVkZGU2IHwgQFJheWRpa2FseCB8IEEyNDA3RCIsImFkZCI6IjE3Mi42NC44MC4xIiwicG9ydCI6Ijg0NDMiLCJpZCI6IjYwNDQxNTQ4LWI2OGUtNDNiMi04MTkxLWUzYjg4NGJlNGIzYyIsImFpZCI6IjAiLCJzY3kiOiJhdXRvIiwibmV0Ijoid3MiLCJ0eXBlIjoiIiwidGxzIjoidGxzIiwiYWxwbiI6IiIsInNuaSI6InYycmF5MS5kb3phcHAueHl6IiwicGF0aCI6Ii9sTW5zWlVONC8iLCJob3N0IjoidjJyYXkxLmRvemFwcC54eXoifQ
```

### SSR（Shadowsocks + ShadowsocksR）

```text
ss://YWVzLTI1Ni1nY206WlJwZ2FCZUd4dEVOSVhndmhwa1pCS3o5R25XUlMyZFljeDlPK2EyaXdOND0@45.86.51.18:19999#shadowsocks-1875022945
ss://YWVzLTI1Ni1nY206WlJwZ2FCZUd4dEVOSVhndmhwa1pCS3o5R25XUlMyZFljeDlPK2EyaXdOND0@45.86.51.18:19999#%F0%9F%87%BA%F0%9F%87%B8US_431%7C1.9MB%2Fs%7CA004-260618%20%5B16f4c5e97fb4%5D
ss://YWVzLTI1Ni1nY206WlJwZ2FCZUd4dEVOSVhndmhwa1pCS3o5R25XUlMyZFljeDlPK2EyaXdOND0=@45.86.51.18:19999#%F0%9F%87%BA%F0%9F%87%B8US-45.86.51.18-0099
ss://YWVzLTI1Ni1nY206WlJwZ2FCZUd4dEVOSVhndmhwa1pCS3o5R25XUlMyZFljeDlPK2EyaXdOND0@45.86.51.18:19999#US
ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M@37.19.198.236:443#shadowsocks-1827146122
ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M@37.19.198.236:443#%F0%9F%87%BA%F0%9F%87%B8US_133%7C1.9MB%2Fs%7CA004-260618%20%5B40dfa7ea8e05%5D
ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M=@37.19.198.236:443#%F0%9F%87%BA%F0%9F%87%B8US-37.19.198.236-0104
ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M@37.19.198.236:443#US
ss://YWVzLTI1Ni1nY206WlJwZ2FCZUd4dEVOSVhndmhwa1pCS3o5R25XUlMyZFljeDlPK2EyaXdOND0@185.230.230.18:19999#shadowsocks-1875023016
ss://YWVzLTI1Ni1nY206WlJwZ2FCZUd4dEVOSVhndmhwa1pCS3o5R25XUlMyZFljeDlPK2EyaXdOND0@185.230.230.18:19999#%F0%9F%87%BA%F0%9F%87%B8US_429%7C1.5MB%2Fs%7CA004-260618%20%5Bbd1e79add0e4%5D
ss://YWVzLTI1Ni1nY206WlJwZ2FCZUd4dEVOSVhndmhwa1pCS3o5R25XUlMyZFljeDlPK2EyaXdOND0=@185.230.230.18:19999#%F0%9F%87%BA%F0%9F%87%B8US-185.230.230.18-0108
ss://YWVzLTI1Ni1nY206WlJwZ2FCZUd4dEVOSVhndmhwa1pCS3o5R25XUlMyZFljeDlPK2EyaXdOND0@185.230.230.18:19999#US
ss://YWVzLTI1Ni1nY206WlJwZ2FCZUd4dEVOSVhndmhwa1pCS3o5R25XUlMyZFljeDlPK2EyaXdOND0@185.230.230.18:19999#%D8%A8%D8%B1%D8%A7%DB%8C%20%D8%A7%D8%AA%D8%B5%D8%A7%D9%84%20%D8%AF%D8%A7%D8%A6%D9%85%DB%8C%20%D8%AC%D9%88%DB%8C%D9%86%20%D8%B4%D9%88%F0%9F%AA%AD%20TelegramID%20%E2%8C%B2Express_freevpn%20%F0%9F%AA%A9`
ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M@37.19.198.244:443#%F0%9F%87%BA%F0%9F%87%B8%20United%20States%2FNew%20York%20%5BGH%3AMahdi0024%2FPro%5D%20%232
ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M@37.19.198.244:443#shadowsocks-1827146742
ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M@37.19.198.244:443#%F0%9F%87%BA%F0%9F%87%B8US_66%7C1.9MB%2Fs%7CA004-260618%20%5B263395b13258%5D
ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M=@37.19.198.244:443#%F0%9F%87%BA%F0%9F%87%B8US-37.19.198.244-0110
ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M@37.19.198.244:443#US
ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M@37.19.198.160:443#%F0%9F%87%BA%F0%9F%87%B8%20United%20States%2FNew%20York%20%5BGH%3AMahdi0024%2FPro%5D
ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M@37.19.198.160:443#shadowsocks-1827146248
ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M@37.19.198.160:443#%F0%9F%87%BA%F0%9F%87%B8US_2%7C2.1MB%2Fs%20%5B0940c1208f74%5D
ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M=@37.19.198.160:443#%F0%9F%87%BA%F0%9F%87%B8US-37.19.198.160-0105
ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M@37.19.198.160:443#US
ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M@37.19.198.243:443#shadowsocks-1827146051
ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M@37.19.198.243:443#%F0%9F%87%BA%F0%9F%87%B8US_5%7C1.8MB%2Fs%20%5Bde8a3340a2be%5D
ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M=@37.19.198.243:443#%F0%9F%87%BA%F0%9F%87%B8US-37.19.198.243-0107
ss://YWVzLTEyOC1nY206c2hhZG93c29ja3M@37.19.198.243:443#US
ss://MjAyMi1ibGFrZTMtYWVzLTI1Ni1nY206UTJZc0l6YzVZa2NoU0Zqc3FVWldyUUFGdHNTcHFmN1h4WXhrRzQrSmJzaz06elQxU2VjUHR0UFkvWFBXNk53aks1V3FsKy82emJjR1NESksyMUprOHVMbz0@216.9.225.189:443#shadowsocks-1853341729
ss://MjAyMi1ibGFrZTMtYWVzLTI1Ni1nY206UTJZc0l6YzVZa2NoU0Zqc3FVWldyUUFGdHNTcHFmN1h4WXhrRzQrSmJzaz06elQxU2VjUHR0UFkvWFBXNk53aks1V3FsKy82emJjR1NESksyMUprOHVMbz0@216.9.225.189:443#US
ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTplRGZON1NPRFFjZUlPbUlBYnRKSnRL@198.98.53.130:443#%F0%9F%87%BA%F0%9F%87%B8%20United%20States%2FStaten%20Island%20%5BGH%3Abarry-far%2FV2r%5D
```

### Clash / Mihomo

```yaml
proxies:
- name: us|81c2|puddincat07@Telegram
  password: 4291c983-c520-46ac-82cc-48f14bef573f
  port: 35013
  server: 129.213.91.185
  skip-cert-verify: true
  sni: 129.213.91.185
  tls: false
  type: hysteria2
- name: 🇺🇸US_431|1.9MB/s|A004-260618 [16f4c5e97fb4]
  cipher: aes-256-gcm
  password: ZRpgaBeGxtENIXgvhpkZBKz9GnWRS2dYcx9O+a2iwN4=
  port: 19999
  server: 45.86.51.18
  sub_tag: A004-260618
  type: ss
  udp: true
- cipher: aes-256-gcm
  name: shadowsocks-1875022945
  password: ZRpgaBeGxtENIXgvhpkZBKz9GnWRS2dYcx9O+a2iwN4=
  port: 19999
  server: 45.86.51.18
  type: ss
  udp: true
- name: 🇺🇸US_7|2.6MB/s
  password: None
  port: 9443
  server: 198.44.135.19
  skip-cert-verify: true
  tls: true
  type: http
- name: 🇺🇸US_289|1.0MB/s|R002-260618 [c29176c7fb94]
  port: 9443
  server: 198.44.135.19
  skip-cert-verify: true
  sub_tag: R002-260618
  tls: true
  type: http
  udp: true
- cipher: aes-128-gcm
  name: shadowsocks-1827146122
  password: shadowsocks
  port: 443
  server: 37.19.198.236
  type: ss
  udp: true
- name: hysteria2-1830343753
  password: 4291c983-c520-46ac-82cc-48f14bef573f
  port: 35013
  server: 129.213.91.185
  skip-cert-verify: true
  sni: 129.213.91.185
  type: hysteria2
- cipher: aes-256-gcm
  name: shadowsocks-1875023016
  password: ZRpgaBeGxtENIXgvhpkZBKz9GnWRS2dYcx9O+a2iwN4=
  port: 19999
  server: 185.230.230.18
  type: ss
  udp: true
- name: '🇺🇸 United States/New York [GH:Mahdi0024/Pro] #2'
  type: ss
  server: 37.19.198.244
  port: 443
  password: shadowsocks
  cipher: aes-128-gcm
  udp: true
- name: 🇺🇸US_429|1.5MB/s|A004-260618 [bd1e79add0e4]
  cipher: aes-256-gcm
  password: ZRpgaBeGxtENIXgvhpkZBKz9GnWRS2dYcx9O+a2iwN4=
  port: 19999
  server: 185.230.230.18
  sub_tag: A004-260618
  type: ss
  udp: true
- name: 🇺🇸US_66|1.9MB/s|A004-260618 [263395b13258]
  cipher: aes-128-gcm
  password: shadowsocks
  port: 443
  server: 37.19.198.244
  sub_tag: A004-260618
  type: ss
  udp: true
- name: 🇺🇸 United States/New York [GH:Mahdi0024/Pro]
  type: ss
  server: 37.19.198.160
  port: 443
  password: shadowsocks
  cipher: aes-128-gcm
  udp: true
- cipher: aes-128-gcm
  name: shadowsocks-1827146051
  password: shadowsocks
  port: 443
  server: 37.19.198.243
  type: ss
  udp: true
- cipher: 2022-blake3-aes-256-gcm
  name: shadowsocks-1853341729
  password: Q2YsIzc5YkchSFjsqUZWrQAFtsSpqf7XxYxkG4+Jbsk=:zT1SecPttPY/XPW6NwjK5Wql+/6zbcGSDJK21Jk8uLo=
  port: 443
  server: 216.9.225.189
  type: ss
  udp: true
- name: 🇺🇸 United States/Staten Island [GH:barry-far/V2r]
  type: ss
  server: 198.98.53.130
  port: 443
  password: eDfN7SODQceIOmIAbtJJtK
  cipher: chacha20-ietf-poly1305
  udp: true
- name: 🇺🇸US_133|1.9MB/s|A004-260618 [40dfa7ea8e05]
  cipher: aes-128-gcm
  password: shadowsocks
  port: 443
  server: 37.19.198.236
  sub_tag: A004-260618
  type: ss
  udp: true
- name: 🇺🇸US_488|1.1MB/s|S001-260618 [f7dbf6629624]
  type: socks5
  server: 20.121.179.183
  port: 3001
  udp: true
- name: 🇺🇸US_488|1.1MB/s|S001-260618 [f7dbf6629624]-2
  password: ''
  port: 3001
  server: 20.121.179.183
  skip-cert-verify: true
  sub_tag: S001-260618
  type: socks5
  username: ''
  udp: true
- name: 🇫🇷FR_49|2.9MB/s|R002-260618 [a676be7daa09]
  port: 443
  server: 172.64.69.89
  skip-cert-verify: true
  sub_tag: R002-260618
  tls: true
  type: http
  udp: true
- name: US
  type: socks5
  server: 20.75.169.229
  port: 3000
  udp: true
- name: 🇺🇸US_447|1.9MB/s|B007-260618 [719341a104ed]
  cipher: aes-256-gcm
  password: ZRpgaBeGxtENIXgvhpkZBKz9GnWRS2dYcx9O+a2iwN4=
  port: 19999
  server: 193.151.163.18
  sub_tag: B007-260618
  type: ss
  udp: true
- name: 🇺🇸US_421|1.6MB/s|A004-260618 [1feecb3b9b0d]
  cipher: rc4-md5
  password: 14fFPrbezE3HDZzsMOr6
  port: 8080
  server: 98.98.79.198
  sub_tag: A004-260618
  type: ss
  udp: true
- name: 🇺🇸 United States/Newark [GH:barry-far/V2r]
  type: ss
  server: 193.151.163.18
  port: 19999
  password: ZRpgaBeGxtENIXgvhpkZBKz9GnWRS2dYcx9O+a2iwN4=
  cipher: aes-256-gcm
  udp: true
- name: CA
  type: vless
  server: 172.67.174.10
  port: 443
  uuid: 2bcfbfba-b446-4ad5-93ad-72af9e008f61
  udp: true
  tls: true
  servername: blackshadow.dpdns.org
  client-fingerprint: chrome
  network: ws
  ws-opts:
    path: /44.209.52.7-443
    headers:
      Host: blackshadow.dpdns.org
- cipher: rc4-md5
  name: shadowsocks-1827964140
  password: 14fFPrbezE3HDZzsMOr6
  port: 8080
  server: 138.197.141.58
  type: ss
  udp: true
- name: 🇺🇸US_435|1.3MB/s|C001-260618 [c9148f5355de]
  cipher: aes-256-gcm
  password: ZRpgaBeGxtENIXgvhpkZBKz9GnWRS2dYcx9O+a2iwN4=
  port: 19999
  server: 193.151.160.18
  sub_tag: C001-260618
  type: ss
  udp: true
- cipher: rc4-md5
  name: shadowsocks-1827147479
  password: 14fFPrbezE3HDZzsMOr6
  port: 8080
  server: 137.184.174.93
  type: ss
  udp: true
- name: 🇺🇸US_430|1.0MB/s|A004-260618 [b62cf4f7c9b4]
  cipher: aes-256-gcm
  password: ZRpgaBeGxtENIXgvhpkZBKz9GnWRS2dYcx9O+a2iwN4=
  port: 19999
  server: 193.151.160.9
  sub_tag: A004-260618
  type: ss
  udp: true
- cipher: aes-256-gcm
  name: shadowsocks-1875129451
  password: ZRpgaBeGxtENIXgvhpkZBKz9GnWRS2dYcx9O+a2iwN4=
  port: 19999
  server: 193.151.160.18
  type: ss
  udp: true
- name: 🇨🇦CA_2|1.2MB/s|A004-260618 [1a7592edd210]
  cipher: rc4-md5
  password: 14fFPrbezE3HDZzsMOr6
  port: 8080
  server: 138.197.141.58
  sub_tag: A004-260618
  type: ss
  udp: true
```

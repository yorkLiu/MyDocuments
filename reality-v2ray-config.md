# Reality VLESS 配置指南（sing-box + reality-ezpz）

## 节点信息
- **协议**：VLESS + Reality + TCP
- **服务器 IP**：`x.x.x.x`
- **端口**：`443`
- **UUID**：`xxx`
- **SNI**：`itunes.apple.com`（推荐）
- **Public Key**：`xxxx`
- **Short ID**：`xxxx`
- **Flow**：`xtls-rprx-vision`
- **Fingerprint**：`chrome`
- **ALPN**：`h2,http/1.1`

## v2rayNG 客户端配置步骤

1. 添加新配置 → 选择 **VLESS**

### 其他推荐设置
- **Mux**：先关闭测试
- **Allow Insecure**：关闭
- 保存后**长按节点 → 测试连接**

## 常见问题解决

- **延迟 -1**：检查 SNI 是否完全一致、Public Key 和 Short ID 是否正确复制。
- **握手失败**：尝试更换 Fingerprint（chrome / firefox），或 Flow 留空。
- **更换 SNI**（服务器端）：
  ```bash
  bash <(curl -sL https://raw.githubusercontent.com/aleskxyz/reality-ezpz/master/reality-ezpz.sh) --domain itunes.apple.com
  ```

## VPS 常用命令

- 查看日志：
  ```bash
  docker logs --tail 100 reality-ezpz-engine-1
  ```

- 重启服务：
  ```bash
  docker restart reality-ezpz-engine-1
  ```

- 显示配置：
  ```bash
  bash <(curl -sL https://raw.githubusercontent.com/aleskxyz/reality-ezpz/master/reality-ezpz.sh) --show-user 默认用户名
  ```

---

**提示**：配置成功后建议开启 BBR 加速以获得更好速度。


## 检查服务状态（正确命令）
```bash
# 1. 查看正确日志（最重要的）
docker logs --tail 200 reality-ezpz-engine-1

# 2. 查看配置文件位置
docker ps

# 3. 获取节点配置（最关键）
docker exec reality-ezpz-engine-1 cat /etc/sing-box/client.json || echo "client.json not found in container"

# 4. 或者直接让脚本显示配置
bash <(curl -sL https://raw.githubusercontent.com/aleskxyz/reality-ezpz/master/reality-ezpz.sh) --show
```

## 临时快速修复（先试这个）
1. 先查看服务器配置
```bash
bash <(curl -sL https://raw.githubusercontent.com/aleskxyz/reality-ezpz/master/reality-ezpz.sh) --show-server-config
```

2. 查看用户配置（推荐这个，带 QR 码）
```bash
bash <(curl -sL https://raw.githubusercontent.com/aleskxyz/reality-ezpz/master/reality-ezpz.sh) --show-user 默认用户名
```
(如果不知道用户名，先执行下面这条列出用户）
```bash
  bash <(curl -sL https://raw.githubusercontent.com/aleskxyz/reality-ezpz/master/reality-ezpz.sh) --list-users
```  

## 重启容器：
```bash
cd /opt/reality-ezpz
docker compose restart
```

## 查看节点配置
```bash
bash <(curl -sL https://raw.githubusercontent.com/aleskxyz/reality-ezpz/master/reality-ezpz.sh) --show
```

# 换端口
**注意事项：**

如果你之前有 Nginx、Apache 或其他服务也在用 443 端口，会冲突导致启动失败。
reality-ezpz 默认就是占用 443，如果你想改成其他端口，可以用以下命令修改：

```bash
bash <(curl -sL https://raw.githubusercontent.com/aleskxyz/reality-ezpz/master/reality-ezpz.sh) --port 8443
```

# 如何更换 UUID、Public Key 和 Short ID
在 reality-ezpz 脚本中，你有以下几种方式更换这些参数：
1. 最简单推荐：重新生成密钥（Regenerate）
执行以下命令（会重新生成 Public Key 和 Short ID，同时可选择新 UUID）：
```bash
bash <(curl -sL https://raw.githubusercontent.com/aleskxyz/reality-ezpz/master/reality-ezpz.sh) --regenerate
```
执行后，脚本会生成新的 Public Key 和 Short ID，UUID 也可能会更新。
生成完成后，运行下面命令查看新配置：
```bash
bash <(curl -sL https://raw.githubusercontent.com/aleskxyz/reality-ezpz/master/reality-ezpz.sh) --show-user 默认用户名
```
（如果不知道用户名，先执行 --list-users）
2. 添加一个新用户（推荐，保留旧用户）
```bash
bash <(curl -sL https://raw.githubusercontent.com/aleskxyz/reality-ezpz/master/reality-ezpz.sh) --add-user 新用户名
```
然后查看新用户配置：
```bash
bash <(curl -sL https://raw.githubusercontent.com/aleskxyz/reality-ezpz/master/reality-ezpz.sh) --show-user 新用户名
```
3. 通过管理菜单操作（最直观）-- 推推使用这个
```bash
bash <(curl -sL https://raw.githubusercontent.com/aleskxyz/reality-ezpz/master/reality-ezpz.sh) --menu
```
进入菜单后可以选择添加用户、重新生成密钥等。

操作完成后建议：

重启容器：Bashdocker restart reality-ezpz-engine-1
把新的 vless:// 完整链接复制到 v2rayNG 中测试。
注意新配置的 SNI、Public Key、Short ID、Flow 等参数要完整复制。

备份好此配置文件，节点信息请妥善保存。

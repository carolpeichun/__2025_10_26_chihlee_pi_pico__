# Pico 連接設定檢查清單

## 目前設定狀態

### ✅ 不需要修改的設定

**`config.py` 中的設定是正確的**，因為：
- `MQTT_BROKER = "localhost"` 是給**樹莓派上的 Flask 應用**使用的
- Flask 應用在樹莓派上運行，所以用 `localhost` 連接到同一台機器上的 MQTT Broker 是正確的

### ⚠️ 需要檢查的設定

為了讓 Pico 能夠連接到樹莓派上的 MQTT Broker，需要確保以下設定：

## 1. MQTT Broker 允許外部連接

### 檢查步驟：

```bash
# 1. 檢查 Mosquitto 是否運行
sudo systemctl status mosquitto

# 2. 檢查 Mosquitto 監聽的介面
sudo netstat -tlnp | grep 1883
# 或
sudo ss -tlnp | grep 1883
```

**預期結果**：應該看到 `0.0.0.0:1883` 或 `:::1883`，表示監聽所有網路介面。

**如果只看到 `127.0.0.1:1883`**，需要修改設定：

### 修改 Mosquitto 設定：

```bash
# 編輯設定檔
sudo nano /etc/mosquitto/mosquitto.conf
```

**添加或修改以下內容：**
```
listener 1883 0.0.0.0
allow_anonymous true
```

**如果已經有 `listener 1883` 但沒有指定 IP，確保沒有綁定到 `127.0.0.1`**

然後重啟服務：
```bash
sudo systemctl restart mosquitto
```

## 2. 防火牆設定

### 檢查防火牆狀態：

```bash
# 如果使用 ufw
sudo ufw status

# 如果使用 iptables
sudo iptables -L -n | grep 1883
```

### 允許 MQTT 連接：

```bash
# 如果使用 ufw
sudo ufw allow 1883/tcp
sudo ufw reload

# 如果使用 firewalld
sudo firewall-cmd --permanent --add-port=1883/tcp
sudo firewall-cmd --reload
```

## 3. 查詢樹莓派 IP 地址

Pico 需要知道樹莓派的 IP 地址才能連接：

```bash
# 方法 1：使用 hostname
hostname -I

# 方法 2：使用 ip 命令
ip addr show | grep "inet " | grep -v 127.0.0.1

# 方法 3：使用 ifconfig（如果已安裝）
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**記下這個 IP 地址，在 Pico 程式碼中使用！**

## 4. 測試 MQTT 連接

### 在樹莓派上測試監聽：

```bash
# 訂閱所有客廳相關主題
mosquitto_sub -h localhost -t "客廳/#" -v
```

### 從另一台電腦測試發送（可選）：

```bash
# 在另一台電腦上（需要安裝 mosquitto-clients）
mosquitto_pub -h <樹莓派IP> -t "客廳/溫度" -m "25.5度"
```

如果樹莓派上的 `mosquitto_sub` 收到訊息，表示設定正確！

## 5. Pico 程式碼設定

在 Pico 的程式碼中，確保：

1. **WiFi 設定正確**：
   ```python
   WIFI_SSID = "你的WiFi名稱"
   WIFI_PASSWORD = "你的WiFi密碼"
   ```

2. **MQTT Broker 設定為樹莓派 IP**：
   ```python
   MQTT_BROKER = "192.168.1.100"  # 改為你的樹莓派 IP
   MQTT_PORT = 1883
   ```

3. **主題名稱正確**：
   ```python
   TOPIC_LIGHT = "客廳/電燈"
   TOPIC_TEMP = "客廳/溫度"
   TOPIC_HUMIDITY = "客廳/溼度"
   ```

## 快速測試流程

1. ✅ 確認 Mosquitto 運行並監聽 `0.0.0.0:1883`
2. ✅ 確認防火牆允許 1883 埠
3. ✅ 查詢並記錄樹莓派 IP 地址
4. ✅ 在樹莓派上執行 `mosquitto_sub -h localhost -t "客廳/#" -v` 監聽
5. ✅ 在 Pico 上執行程式碼發送測試訊息
6. ✅ 確認樹莓派收到訊息

## 常見問題

### Q: Pico 無法連接到 MQTT Broker
- 檢查 Pico 和樹莓派是否在同一個 WiFi 網路
- 檢查樹莓派 IP 地址是否正確
- 檢查防火牆設定
- 檢查 Mosquitto 是否監聽外部連接

### Q: 樹莓派上的 Flask 應用無法接收訊息
- 檢查 `config.py` 中的 `MQTT_BROKER = "localhost"` 是否正確
- 檢查 Mosquitto 是否運行
- 檢查 Flask 應用是否正常啟動並連接 MQTT

### Q: 訊息格式問題
- 參考 `PICO_SETUP.md` 中的訊息格式說明
- 系統支援純文字和 JSON 兩種格式
- 確保主題名稱正確（`客廳/電燈`、`客廳/溫度`、`客廳/溼度`）


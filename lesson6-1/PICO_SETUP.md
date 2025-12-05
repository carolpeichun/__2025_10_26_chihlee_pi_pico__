# Pico MQTT 發送設定指南

本文件說明如何讓 Raspberry Pi Pico 發送訊息到樹莓派上的 MQTT Broker。

## 訊息格式說明

系統支援兩種訊息格式，Pico 可以選擇最適合的方式：

### 方式一：純文字格式（推薦，最簡單）

直接發送數值或狀態字串即可，系統會自動解析：

#### 電燈狀態
- **主題**：`客廳/電燈`
- **訊息內容**：`"開"` 或 `"關"` 或 `"on"` 或 `"off"`

#### 溫度
- **主題**：`客廳/溫度`
- **訊息內容**：`"26.5"` 或 `"26.5度"` 或 `26.5`（數值）

#### 溼度
- **主題**：`客廳/溼度`
- **訊息內容**：`"60"` 或 `"60%"` 或 `60`（數值）

### 方式二：JSON 格式（結構化資料）

#### 單一數據
```json
// 電燈狀態
{"status": "開"} 或 {"value": "開"}

// 溫度
{"temperature": 26.5} 或 {"value": 26.5}

// 溼度
{"humidity": 60.0} 或 {"value": 60.0}
```

#### 組合數據（一次發送多個）
```json
{
  "light": "開",
  "temperature": 26.5,
  "humidity": 60.0
}
```

## Pico 程式碼範例

### 範例 1：使用純文字格式（最簡單）

```python
import network
import time
from umqtt.simple import MQTTClient

# WiFi 設定
WIFI_SSID = "你的WiFi名稱"
WIFI_PASSWORD = "你的WiFi密碼"

# MQTT 設定（請改為樹莓派的 IP 地址）
MQTT_BROKER = "192.168.1.160"  # 改為樹莓派的 IP
MQTT_PORT = 1883
MQTT_CLIENT_ID = "pico_client"

# MQTT 主題
TOPIC_LIGHT = "客廳/電燈"
TOPIC_TEMP = "客廳/溫度"
TOPIC_HUMIDITY = "客廳/溼度"

def connect_wifi():
    """連接 WiFi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    print("正在連接 WiFi...")
    while not wlan.isconnected():
        time.sleep(1)
    
    print(f"WiFi 連接成功！IP: {wlan.ifconfig()[0]}")
    return wlan

def main():
    # 連接 WiFi
    wlan = connect_wifi()
    
    # 建立 MQTT 客戶端
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT)
    
    try:
        # 連接到 MQTT Broker
        print(f"正在連接 MQTT Broker: {MQTT_BROKER}")
        client.connect()
        print("MQTT 連接成功！")
        
        # 模擬感測器數據（請替換為實際的感測器讀取）
        light_status = "開"
        temperature = 26.5
        humidity = 60.0
        
        while True:
            # 發送電燈狀態（純文字）
            client.publish(TOPIC_LIGHT, light_status)
            print(f"已發送電燈狀態: {light_status}")
            
            # 發送溫度（純文字，可帶單位）
            temp_str = f"{temperature}度"
            client.publish(TOPIC_TEMP, temp_str)
            print(f"已發送溫度: {temp_str}")
            
            # 發送溼度（純文字，可帶 %）
            hum_str = f"{humidity}%"
            client.publish(TOPIC_HUMIDITY, hum_str)
            print(f"已發送溼度: {hum_str}")
            
            # 等待 5 秒後再次發送
            time.sleep(5)
            
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        client.disconnect()
        wlan.disconnect()

if __name__ == "__main__":
    main()
```

### 範例 2：使用 JSON 格式（組合數據）

```python
import network
import time
import json
from umqtt.simple import MQTTClient

# WiFi 設定
WIFI_SSID = "你的WiFi名稱"
WIFI_PASSWORD = "你的WiFi密碼"

# MQTT 設定（請改為樹莓派的 IP 地址）
MQTT_BROKER = "192.168.1.160"  # 改為樹莓派的 IP
MQTT_PORT = 1883
MQTT_CLIENT_ID = "pico_client"

# MQTT 主題（使用其中一個主題發送組合數據）
TOPIC_SENSOR = "客廳/溫度"  # 可以用任何一個主題

def connect_wifi():
    """連接 WiFi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    print("正在連接 WiFi...")
    while not wlan.isconnected():
        time.sleep(1)
    
    print(f"WiFi 連接成功！IP: {wlan.ifconfig()[0]}")
    return wlan

def main():
    # 連接 WiFi
    wlan = connect_wifi()
    
    # 建立 MQTT 客戶端
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT)
    
    try:
        # 連接到 MQTT Broker
        print(f"正在連接 MQTT Broker: {MQTT_BROKER}")
        client.connect()
        print("MQTT 連接成功！")
        
        while True:
            # 讀取感測器數據（請替換為實際的感測器讀取）
            # 例如：使用 DHT22 或 DHT11
            temperature = 26.5  # 實際讀取
            humidity = 60.0     # 實際讀取
            light_status = "開"  # 實際讀取
            
            # 建立 JSON 格式的組合數據
            data = {
                "light": light_status,
                "temperature": temperature,
                "humidity": humidity
            }
            
            # 發送 JSON 字串
            json_str = json.dumps(data)
            client.publish(TOPIC_SENSOR, json_str)
            print(f"已發送組合數據: {json_str}")
            
            # 等待 5 秒後再次發送
            time.sleep(5)
            
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        client.disconnect()
        wlan.disconnect()

if __name__ == "__main__":
    main()
```

### 範例 3：使用 DHT22 感測器（實際應用）

```python
import network
import time
import json
from umqtt.simple import MQTTClient
from dht import DHT22
from machine import Pin

# WiFi 設定
WIFI_SSID = "你的WiFi名稱"
WIFI_PASSWORD = "你的WiFi密碼"

# MQTT 設定
MQTT_BROKER = "192.168.1.160"  # 改為樹莓派的 IP
MQTT_PORT = 1883
MQTT_CLIENT_ID = "pico_dht22"

# 感測器設定
DHT_PIN = 16  # 根據你的接線調整
dht = DHT22(Pin(DHT_PIN))

# MQTT 主題
TOPIC_TEMP = "客廳/溫度"
TOPIC_HUMIDITY = "客廳/溼度"

def connect_wifi():
    """連接 WiFi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    print("正在連接 WiFi...")
    while not wlan.isconnected():
        time.sleep(1)
    
    print(f"WiFi 連接成功！IP: {wlan.ifconfig()[0]}")
    return wlan

def main():
    # 連接 WiFi
    wlan = connect_wifi()
    
    # 建立 MQTT 客戶端
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT)
    
    try:
        # 連接到 MQTT Broker
        print(f"正在連接 MQTT Broker: {MQTT_BROKER}")
        client.connect()
        print("MQTT 連接成功！")
        
        while True:
            try:
                # 讀取 DHT22 數據
                dht.measure()
                temperature = dht.temperature()
                humidity = dht.humidity()
                
                # 發送溫度（純文字格式）
                temp_str = f"{temperature:.1f}度"
                client.publish(TOPIC_TEMP, temp_str)
                print(f"已發送溫度: {temp_str}")
                
                # 發送溼度（純文字格式）
                hum_str = f"{humidity:.1f}%"
                client.publish(TOPIC_HUMIDITY, hum_str)
                print(f"已發送溼度: {hum_str}")
                
            except Exception as e:
                print(f"讀取感測器錯誤: {e}")
            
            # 等待 5 秒後再次讀取
            time.sleep(5)
            
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        client.disconnect()
        wlan.disconnect()

if __name__ == "__main__":
    main()
```

## 重要設定檢查

### 1. 樹莓派 IP 地址

在 Pico 程式碼中，需要將 `MQTT_BROKER` 設定為樹莓派的 IP 地址，而不是 `localhost`。

**如何查詢樹莓派 IP：**
```bash
# 在樹莓派上執行
hostname -I
# 或
ip addr show
```

### 2. MQTT Broker 設定

確保樹莓派上的 MQTT Broker（例如 Mosquitto）允許外部連接：

**檢查 Mosquitto 設定：**
```bash
# 檢查 Mosquitto 是否運行
sudo systemctl status mosquitto

# 檢查監聽的介面（應該包含 0.0.0.0 或你的網路介面）
sudo netstat -tlnp | grep 1883
```

**如果需要允許外部連接，編輯 `/etc/mosquitto/mosquitto.conf`：**
```
listener 1883 0.0.0.0
allow_anonymous true
```

然後重啟服務：
```bash
sudo systemctl restart mosquitto
```

### 3. 防火牆設定

確保樹莓派的防火牆允許 MQTT 連接（埠號 1883）：

```bash
# 如果使用 ufw
sudo ufw allow 1883/tcp

# 如果使用 iptables
sudo iptables -A INPUT -p tcp --dport 1883 -j ACCEPT
```

## 測試連接

在 Pico 上傳並執行程式碼後，應該會看到：
1. WiFi 連接成功的訊息
2. MQTT 連接成功的訊息
3. 定期發送數據的訊息

在樹莓派上，可以監聽 MQTT 訊息來測試：
```bash
mosquitto_sub -h localhost -t "客廳/#" -v
```

如果看到 Pico 發送的訊息，表示連接成功！

## 注意事項

1. **主題名稱必須正確**：使用 `客廳/電燈`、`客廳/溫度`、`客廳/溼度`
2. **訊息格式靈活**：系統會自動解析純文字或 JSON 格式
3. **網路連接**：確保 Pico 和樹莓派在同一個 WiFi 網路中
4. **MQTT Client ID**：每個 Pico 應該使用不同的 Client ID，避免衝突


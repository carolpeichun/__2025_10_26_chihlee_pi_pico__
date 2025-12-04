# 智慧家居監控系統

本專案是一個基於 Flask 的物聯網監控應用程式，可在樹莓派上運行，透過 MQTT 協議訂閱並即時顯示智慧家居設備的狀態資訊。

## 功能特色

- **即時監控**：透過 Web 介面即時顯示電燈狀態、客廳溫度和溼度
- **圖表視覺化**：使用 Chart.js 繪製溫溼度歷史趨勢圖表
- **數據儲存**：自動將所有接收到的 MQTT 數據儲存為 Excel 檔案
- **MQTT 訂閱**：作為 MQTT 訂閱者，接收並處理來自 MQTT Broker 的訊息

## 系統需求

- Python 3.10 或更高版本（建議 3.11）
- 樹莓派（Raspberry Pi）或相容的 Linux 系統
- MQTT Broker（例如 Mosquitto）
 - 可連網的瀏覽器（支援 Socket.IO 與 ES6）

## 安裝步驟

### 1. 安裝 Python 套件

確保已安裝所需的 Python 套件。如果專案根目錄已有 `pyproject.toml`，可以使用以下命令：

```bash
pip install -r requirements.txt
```

或者從專案根目錄安裝：

```bash
pip install -e ..
```

### 2. 確認 MQTT Broker

確保 MQTT Broker 正在運行。預設設定為 `localhost:1883`。如果需要修改，請編輯 `config.py` 檔案。

## 配置說明

編輯 `config.py` 檔案以自訂設定：

```python
# MQTT Broker 設定
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

# MQTT 訂閱主題（使用萬用字元訂閱所有客廳相關主題）
MQTT_SUBSCRIBE_TOPIC = "客廳/#"  # 訂閱所有以 "客廳/" 開頭的主題

# 實際的主題名稱（用於判斷數據類型）
MQTT_TOPICS = {
    "light": "客廳/電燈",       # 電燈狀態主題
    "temperature": "客廳/溫度", # 溫度主題
    "humidity": "客廳/溼度"     # 溼度主題
}

# Excel 儲存設定
import os
_config_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(_config_dir, "data")  # 使用相對於專案的 data 資料夾
EXCEL_FILENAME = "sensor_data.xlsx"           # Excel 檔案名稱
MAX_RECORDS = 300                             # 最多保留最新 300 筆資料

# Flask 設定
FLASK_HOST = "0.0.0.0"  # 允許外部訪問
FLASK_PORT = 5000       # Web 服務埠號

# 注意：
# - 開發時可以將 FLASK_DEBUG 設為 True，方便自動重載程式碼
# - 但在會進行檔案寫入（例如 Excel）的情況下，請設定為 False，
#   以避免 debug reloader 產生兩個進程同時寫入同一個檔案，造成檔案損壞
FLASK_DEBUG = False
```

## 執行應用程式

在 `lesson6-1` 目錄下執行：

```bash
python app.py
```

應用程式啟動後，開啟瀏覽器訪問：

```
http://localhost:5000
```

或從其他設備訪問（使用樹莓派的 IP 位址）：

```
http://<樹莓派IP>:5000
```

啟動後，後端會：

- 初始化 `DataStorage`，自動建立 `data/sensor_data.xlsx` 並保留最新 **300 筆** 資料
- 啟動 `MQTTClient`，以訂閱主題 `客廳/#` 並自動判斷是電燈／溫度／溼度
- 啟動 Flask-SocketIO Web 服務，透過 WebSocket 即時推送感測數據與圖表更新

## 專案結構

```
lesson6-1/
├── PRD.md                 # 產品需求文檔
├── app.py                 # Flask 主應用程式
├── mqtt_client.py         # MQTT 訂閱者模組
├── data_storage.py        # Excel 儲存功能
├── mqtt_publisher_test.py # MQTT 測試發送程式（每數秒發送一次模擬數據）
├── create_sample_data.py  # （選用）建立範例 Excel 數據檔案
├── config.py              # 配置檔案
├── requirements.txt       # Python 套件依賴
├── README.md              # 本說明文件
├── templates/
│   └── index.html         # 前端介面
├── static/
│   └── css/
│       └── style.css      # 樣式檔案
└── data/                  # Excel 檔案儲存目錄（自動建立）
    └── sensor_data.xlsx   # 儲存的感測器數據（自動建立，最多保留 300 筆）
```

## MQTT 訊息格式

應用程式支援 JSON 格式的 MQTT 訊息。範例：

### 電燈狀態
```json
{
  "status": "on"
}
```
或
```json
{
  "value": "開"
}
```

### 溫度
```json
{
  "temperature": 25.5
}
```
或
```json
{
  "value": 25.5
}
```

### 溼度
```json
{
  "humidity": 60.0
}
```
或
```json
{
  "value": 60.0
}
```

### 組合訊息
也可以一次發送多個數據：
```json
{
  "light": "on",
  "temperature": 25.5,
  "humidity": 60.0
}
```

## 使用說明

1. **啟動應用程式**：執行 `python app.py`
2. **連接 MQTT**：應用程式會自動連接到 MQTT Broker 並訂閱設定的主題
3. **查看監控介面**：在瀏覽器中開啟 Web 介面
4. **接收數據**：當 MQTT 訊息到達時，介面會自動更新
5. **查看歷史數據**：所有數據會自動儲存到 `data/sensor_data.xlsx`

## 注意事項

- 確保 MQTT Broker 正在運行且可訪問
- 檢查防火牆設定，確保允許訪問 Flask 服務的埠號（預設 5000）
- Excel 檔案會自動建立，無需手動建立 `data` 目錄
- 如果 MQTT 連接失敗，請檢查 `config.py` 中的 Broker 設定

## 疑難排解

### MQTT 連接失敗
- 確認 MQTT Broker 正在運行：`systemctl status mosquitto`（如果使用 Mosquitto）
- 檢查防火牆設定
- 確認 `config.py` 中的 Broker 位址和埠號正確

### 無法訪問 Web 介面
- 確認應用程式正在運行
- 檢查埠號是否被其他程式占用
- 如果從其他設備訪問，確認使用正確的 IP 位址

### 數據未更新
- 確認 MQTT 訊息正在發送到正確的主題
- 檢查瀏覽器控制台是否有錯誤訊息
- 確認 WebSocket 連接正常（查看頁面上的連接狀態）

## 授權

本專案為教學用途。


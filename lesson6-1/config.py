"""
配置檔案
定義 MQTT 連接設定、訂閱主題和應用程式配置
"""

# MQTT Broker 設定
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

# MQTT 訂閱主題（使用萬用字元訂閱所有客廳相關主題）
MQTT_SUBSCRIBE_TOPIC = "客廳/#"  # 訂閱所有以 "客廳/" 開頭的主題

# 實際的主題名稱（用於判斷數據類型）
MQTT_TOPICS = {
    "light": "客廳/電燈",           # 電燈狀態主題
    "temperature": "客廳/溫度",     # 溫度主題
    "humidity": "客廳/溼度"         # 溼度主題
}

# Excel 儲存設定
# 使用相對於此配置檔案所在目錄的路徑，確保無論從哪裡執行都能找到正確的資料夾
import os
_config_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(_config_dir, "data")
EXCEL_FILENAME = "sensor_data.xlsx"
MAX_RECORDS = 300  # 最多保留的資料筆數（超過此數量會刪除最舊的資料）

# Flask 設定
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000

# 注意：
# - 開發時可以將 FLASK_DEBUG 設為 True，方便自動重載程式碼
# - 但在會進行檔案寫入（例如 Excel）的情況下，請設定為 False，
#   以避免 debug reloader 產生兩個進程同時寫入同一個檔案，造成檔案損壞
FLASK_DEBUG = False


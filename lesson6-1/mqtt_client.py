"""
MQTT 訂閱者模組
負責連接 MQTT Broker、訂閱主題並處理接收到的訊息
"""

import json
import re
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO
import config


class MQTTClient:
    """MQTT 客戶端類別，處理訂閱和訊息接收"""
    
    def __init__(self, socketio: SocketIO, data_storage):
        """
        初始化 MQTT 客戶端
        
        Args:
            socketio: Flask-SocketIO 實例，用於推送即時數據
            data_storage: DataStorage 實例，用於儲存數據
        """
        self.socketio = socketio
        self.data_storage = data_storage
        self.client = None
        self.current_data = {
            "light": None,
            "temperature": None,
            "humidity": None
        }
        self._setup_client()
    
    def _setup_client(self):
        """設定 MQTT 客戶端"""
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
    
    def _on_connect(self, client, userdata, flags, rc):
        """MQTT 連接回調函數"""
        if rc == 0:
            print("MQTT 連接成功")
            # 訂閱萬用字元主題
            client.subscribe(config.MQTT_SUBSCRIBE_TOPIC)
            print(f"已訂閱主題: {config.MQTT_SUBSCRIBE_TOPIC}")
        else:
            print(f"MQTT 連接失敗，錯誤代碼: {rc}")
    
    def _on_message(self, client, userdata, msg):
        """MQTT 訊息接收回調函數"""
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            
            print(f"收到訊息 - 主題: {topic}, 內容: {payload}")
            
            # 解析 JSON 訊息
            try:
                data = json.loads(payload)
            except json.JSONDecodeError:
                # 如果不是 JSON，建立簡單的字典
                data = {"value": payload}
            
            # 根據主題更新當前數據
            self._update_current_data(topic, data)
            
            # 儲存到 Excel
            self.data_storage.save_mqtt_message(topic, data)
            
            # 透過 SocketIO 推送即時數據到前端
            self._emit_data_update()
            
        except Exception as e:
            print(f"處理 MQTT 訊息時發生錯誤: {e}")
    
    def _update_current_data(self, topic, data):
        """根據主題更新當前數據"""
        def _to_float(value):
            """嘗試從各種格式中取出數值（例如 '26度' 也能解析為 26）"""
            if value is None:
                return None
            try:
                # 先處理已是數值的情況
                if isinstance(value, (int, float)):
                    return float(value)
                s = str(value)
                s = s.strip()
                # 從字串中擷取第一個數字（含小數點與負號）
                m = re.search(r"-?\d+(?:\.\d+)?", s)
                if not m:
                    return None
                return float(m.group(0))
            except Exception:
                return None

        # 根據主題名稱判斷數據類型
        if topic == config.MQTT_TOPICS["light"] or "電燈" in topic:
            # 電燈狀態
            light_value = data.get("status", data.get("value", data.get("light", "")))
            if light_value is not None:
                self.current_data["light"] = str(light_value)
        
        elif topic == config.MQTT_TOPICS["temperature"] or "溫度" in topic:
            # 溫度數據
            temp_value = data.get("temperature", data.get("value", data.get("temp")))
            parsed = _to_float(temp_value)
            if parsed is not None:
                self.current_data["temperature"] = parsed
        
        elif topic == config.MQTT_TOPICS["humidity"] or "溼度" in topic:
            # 溼度數據
            hum_value = data.get("humidity", data.get("value", data.get("hum")))
            parsed = _to_float(hum_value)
            if parsed is not None:
                self.current_data["humidity"] = parsed
        
        # 如果訊息包含多個數據，一起更新
        if isinstance(data, dict):
            if "light" in data or "light_status" in data:
                self.current_data["light"] = str(data.get("light", data.get("light_status", "")))
            if "temperature" in data or "temp" in data:
                temp = data.get("temperature", data.get("temp"))
                parsed = _to_float(temp)
                if parsed is not None:
                    self.current_data["temperature"] = parsed
            if "humidity" in data or "hum" in data:
                hum = data.get("humidity", data.get("hum"))
                parsed = _to_float(hum)
                if parsed is not None:
                    self.current_data["humidity"] = parsed
    
    def _emit_data_update(self):
        """透過 SocketIO 推送數據更新到前端"""
        self.socketio.emit('data_update', {
            'light': self.current_data["light"],
            'temperature': self.current_data["temperature"],
            'humidity': self.current_data["humidity"]
        })
    
    def _on_disconnect(self, client, userdata, rc):
        """MQTT 斷線回調函數"""
        print("MQTT 連接已斷開")
    
    def connect(self):
        """連接到 MQTT Broker"""
        try:
            self.client.connect(
                config.MQTT_BROKER,
                config.MQTT_PORT,
                config.MQTT_KEEPALIVE
            )
            # 在背景執行網路循環
            self.client.loop_start()
        except Exception as e:
            print(f"連接 MQTT Broker 時發生錯誤: {e}")
    
    def disconnect(self):
        """斷開 MQTT 連接"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
    
    def get_current_data(self):
        """取得當前數據"""
        return self.current_data.copy()


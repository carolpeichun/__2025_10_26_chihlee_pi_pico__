"""
Flask 主應用程式
整合 MQTT 客戶端、數據儲存和 Web 介面
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
import config
from mqtt_client import MQTTClient
from data_storage import DataStorage

# 初始化 Flask 應用程式
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# 初始化 SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# 初始化數據儲存
data_storage = DataStorage()

# 初始化 MQTT 客戶端
mqtt_client = None


@app.route('/')
def index():
    """首頁路由"""
    return render_template('index.html')


@app.route('/api/history')
def get_history():
    """取得歷史數據 API"""
    try:
        limit = int(request.args.get('limit', 100))
        history_data = data_storage.get_history_data(limit=limit)
        return jsonify({
            'success': True,
            'data': history_data,
            'count': len(history_data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/latest')
def get_latest():
    """取得最新數據 API"""
    try:
        latest_data = data_storage.get_latest_data()
        return jsonify({
            'success': True,
            'data': latest_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@socketio.on('connect')
def handle_connect():
    """處理 WebSocket 連接"""
    print('客戶端已連接')
    # 發送當前數據給新連接的客戶端
    if mqtt_client:
        current_data = mqtt_client.get_current_data()
        socketio.emit('data_update', current_data)


@socketio.on('disconnect')
def handle_disconnect():
    """處理 WebSocket 斷線"""
    print('客戶端已斷開連接')


def init_mqtt():
    """初始化 MQTT 客戶端"""
    global mqtt_client
    mqtt_client = MQTTClient(socketio, data_storage)
    mqtt_client.connect()


if __name__ == '__main__':
    # 初始化 MQTT 連接
    init_mqtt()
    
    # 啟動 Flask 應用程式
    try:
        # 說明：
        # - 在啟用 debug 時，如果使用 reloader，Flask 會啟動兩個進程
        #   這會導致 MQTT 客戶端與 Excel 寫入被執行兩次，進而損壞檔案
        # - 因此這裡即使在 debug 模式下，也關閉 use_reloader，確保只有一個進程在跑
        socketio.run(
            app,
            host=config.FLASK_HOST,
            port=config.FLASK_PORT,
            debug=config.FLASK_DEBUG,
            use_reloader=False,
        )
    except KeyboardInterrupt:
        print("\n正在關閉應用程式...")
        if mqtt_client:
            mqtt_client.disconnect()


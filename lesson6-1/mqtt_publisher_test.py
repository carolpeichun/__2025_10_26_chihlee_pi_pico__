"""
MQTT 測試發送程式
每 2 秒自動發送一次電燈狀態、溫度與溼度到客廳相關主題。

用途：
- 測試 lesson6-1 Flask 應用程式的即時顯示與歷史儲存功能
"""

import time
import random

import paho.mqtt.client as mqtt

import config


def main():
    # 建立 MQTT Client
    client = mqtt.Client()

    print("連接到 MQTT Broker...")
    client.connect(config.MQTT_BROKER, config.MQTT_PORT, config.MQTT_KEEPALIVE)
    print(f"已連接：{config.MQTT_BROKER}:{config.MQTT_PORT}")

    # 初始狀態
    light_on = True

    try:
        while True:
            # 切換電燈狀態（每次迴圈翻轉）
            light_on = not light_on
            light_status_str = "開" if light_on else "關"

            # 模擬溫度（24~30 度之間隨機小幅變動）
            temperature = round(random.uniform(24, 30), 1)

            # 模擬溼度（50~70% 之間隨機小幅變動）
            humidity = round(random.uniform(50, 70), 1)

            # 發送電燈狀態（純文字）
            client.publish(config.MQTT_TOPICS["light"], light_status_str, qos=0)

            # 發送溫度（帶中文單位，測試我們的字串解析）
            client.publish(config.MQTT_TOPICS["temperature"], f"{temperature}度", qos=0)

            # 發送溼度（帶 % 號）
            client.publish(config.MQTT_TOPICS["humidity"], f"{humidity}%", qos=0)

            print(
                f"已發送 -> 電燈: {light_status_str}, "
                f"溫度: {temperature}度, 溼度: {humidity}%"
            )

            # 每 2 秒發送一次
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n停止測試發送程式")


if __name__ == "__main__":
    main()




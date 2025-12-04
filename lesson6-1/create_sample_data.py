"""
建立範例 Excel 數據檔案
用於測試和展示應用程式功能
"""

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from datetime import datetime, timedelta
import os
import random

# 確保資料夾存在
os.makedirs('data', exist_ok=True)

# 建立工作簿
wb = Workbook()
ws = wb.active
ws.title = '感測器數據'

# 設定標題列
headers = ['時間戳記', '電燈狀態', '溫度 (°C)', '溼度 (%)']
ws.append(headers)

# 設定標題列樣式
for cell in ws[1]:
    cell.font = Font(bold=True)
    cell.alignment = Alignment(horizontal='center')

# 調整欄寬
ws.column_dimensions['A'].width = 20
ws.column_dimensions['B'].width = 15
ws.column_dimensions['C'].width = 15
ws.column_dimensions['D'].width = 15

# 產生範例數據（過去10分鐘，每2秒一筆）
base_time = datetime.now() - timedelta(minutes=10)
data_count = 300  # 10分鐘 * 60秒 / 2秒 = 300筆

for i in range(data_count):
    timestamp = base_time + timedelta(seconds=i*2)
    timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    # 模擬電燈狀態（每30秒變化一次）
    light_status = '開' if (i // 15) % 2 == 0 else '關'
    
    # 模擬溫度（20-30度之間，有波動）
    base_temp = 25
    temp_variation = 5 * (i % 60) / 60  # 週期性變化
    temperature = round(base_temp + temp_variation + random.uniform(-1, 1), 1)
    
    # 模擬溼度（50-70%之間，有波動）
    base_hum = 60
    hum_variation = 10 * (i % 40) / 40  # 週期性變化
    humidity = round(base_hum + hum_variation + random.uniform(-2, 2), 1)
    
    ws.append([timestamp_str, light_status, temperature, humidity])

# 儲存檔案
excel_path = 'data/sensor_data.xlsx'
wb.save(excel_path)
print(f'範例 Excel 檔案已建立：{excel_path}')
print(f'共產生 {data_count} 筆範例數據（過去10分鐘，每2秒一筆）')



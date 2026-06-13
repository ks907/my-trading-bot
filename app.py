import os
import json
import time
import gspread
import ccxt
from oauth2client.service_account import ServiceAccountCredentials

# 1. 비트겟 연결 (Render 환경변수에서 불러옴)
exchange = ccxt.bitget({
    'apiKey': os.environ.get('BITGET_API_KEY'),
    'secret': os.environ.get('BITGET_SECRET'),
    'password': os.environ.get('BITGET_PASSPHRASE'),
    'enableRateLimit': True,
})

# 2. 구글 시트 연결 (Render 환경변수에서 JSON 내용 불러옴)
# app.py 상단의 scope를 이렇게 바꿔보세요
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
json_key_dict = json.loads(os.environ['GOOGLE_APPLICATION_CREDENTIALS_JSON'])
creds = ServiceAccountCredentials.from_json_keyfile_dict(json_key_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/11srfi3OC08qbqrU5IuMs5vFap_wWMiK5jeye9vxWGCk/edit?gid=0#gid=0").sheet1

print("봇이 시작되었습니다. 신호를 기다리는 중...")

while True:
    try:
        # 3. 시트 확인
        cell_value = sheet.cell(2, 1).value
        
        if cell_value and "buy" in cell_value.lower():
            print("매수 신호 감지! 주문 실행 중...")
            exchange.create_market_buy_order('BTC/USDT', 0.001)
            
            # 4. 주문 후 셀 비우기
            sheet.update_cell(2, 1, "")
            print("주문 완료 및 시트 초기화.")
            
    except Exception as e:
        print(f"오류 발생: {e}")
        
    time.sleep(5) # 5초마다 확인

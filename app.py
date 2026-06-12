import time
import gspread
import ccxt
from oauth2client.service_account import ServiceAccountCredentials

# 1. 비트겟 연결 설정
exchange = ccxt.bitget({
    'apiKey': '회원님의_비트겟_API_KEY',
    'secret': '회원님의_비트겟_SECRET_KEY',
    'password': '회원님의_API_PASSPHRASE',
    'enableRateLimit': True,
})

# 2. 구글 시트 연결
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Trading_Signal").sheet1

print("봇이 시작되었습니다. 신호를 기다리는 중...")

while True:
    # 3. 시트 확인 (A2 셀)
    cell_value = sheet.cell(2, 1).value
    
    if cell_value and "buy" in cell_value:
        print("매수 신호 감지! 주문 실행 중...")
        # 4. 비트겟 매수 주문
        exchange.create_market_buy_order('BTC/USDT', 0.001) # 수량은 적절히 조정하세요
        
        # 5. 주문 후 셀 비우기 (중복 방지)
        sheet.update_cell(2, 1, "")
        print("주문 완료 및 시트 초기화.")
        
    time.sleep(5) # 5초마다 확인

import os
import json
import time
import gspread
import ccxt
import threading
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask

app = Flask(__name__)

@app.route('/')
def keep_alive():
    return "봇이 정상 작동 중입니다!"

def run_bot():
    try:
        # 1. 비트겟 연결 설정 (비트겟 전용 옵션 추가)
        exchange = ccxt.bitget({
            'apiKey': os.environ.get('BITGET_API_KEY'),
            'secret': os.environ.get('BITGET_SECRET'),
            'password': os.environ.get('BITGET_PASSPHRASE'),
            'enableRateLimit': True,
            'options': {
                'createMarketBuyOrderRequiresPrice': False, # 👈 에러를 해결하는 핵심 옵션입니다!
            },
        })

        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        json_key_dict = json.loads(os.environ['GOOGLE_APPLICATION_CREDENTIALS_JSON'])
        creds = ServiceAccountCredentials.from_json_keyfile_dict(json_key_dict, scope)
        client = gspread.authorize(creds)
        
        # 👇 여기에 회원님의 구글 시트 URL을 다시 넣어주세요! 👇
        sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/11srfi3OC08qbqrU5IuMs5vFap_wWMiK5jeye9vxWGCk/edit?gid=0#gid=0").sheet1
        
        print("봇이 시작되었습니다. 신호를 기다리는 중...")
        
        while True:
            try:
                cell_value = sheet.cell(2, 1).value
                if cell_value and "buy" in cell_value.lower():
                    print("매수 신호 감지! 주문 실행 중...")
                    
                    # 👈 중요: 이제 수량(0.001)이 아니라 '원하는 금액(USDT)'을 적습니다.
                    # 숫자 10은 '10달러(USDT)어치 비트코인을 즉시 사겠다'는 뜻입니다.
                    # 금액을 바꾸고 싶다면 이 숫자를 원하시는 대로 바꾸시면 됩니다. (비트겟 최소 주문은 보통 5달러 이상)
                    exchange.create_market_buy_order('BTC/USDT', 10)
                    
                    sheet.update_cell(2, 1, "")
                    print("주문 완료 및 시트 초기화.")
            except Exception as e:
                print(f"주문 실행 중 오류 발생: {e}")
            time.sleep(5)
            
    except Exception as e:
        print(f"봇 초기 설정 오류: {e}")

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

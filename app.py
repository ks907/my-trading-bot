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
        exchange = ccxt.bitget({
            'apiKey': os.environ.get('BITGET_API_KEY'),
            'secret': os.environ.get('BITGET_SECRET'),
            'password': os.environ.get('BITGET_PASSPHRASE'),
            'enableRateLimit': True,
        })

        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        json_key_dict = json.loads(os.environ['GOOGLE_APPLICATION_CREDENTIALS_JSON'])
        creds = ServiceAccountCredentials.from_json_keyfile_dict(json_key_dict, scope)
        client = gspread.authorize(creds)
        
        # 👇 여기에 회원님의 구글 시트 URL을 잊지 말고 넣어주세요! 👇
        sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/11srfi3OC08qbqrU5IuMs5vFap_wWMiK5jeye9vxWGCk/edit?gid=0#gid=0").sheet1
        
        print("봇이 시작되었습니다. 신호를 기다리는 중...")
        
        while True:
            try:
                # A2 셀 확인 (2행, 1열)
                cell_value = sheet.cell(2, 1).value
                if cell_value and "buy" in cell_value.lower():
                    print("매수 신호 감지! 주문 실행 중...")
                    exchange.create_market_buy_order('BTC/USDT', 0.001)
                    sheet.update_cell(2, 1, "")
                    print("주문 완료 및 시트 초기화.")
            except Exception as e:
                # 👇 조용히 넘기지 않고, 무슨 에러인지 로그에 찍도록 수정했습니다 👇
                print(f"주문 실행 중 오류 발생: {e}")
            time.sleep(5)
            
    except Exception as e:
        print(f"봇 초기 설정 오류: {e}")

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

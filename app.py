from flask import Flask, request, jsonify
import ccxt

app = Flask(__name__)

# 비트겟 API 연결 (나중에 서버에서 설정할 비밀 값들입니다)
import os
exchange = ccxt.bitget({
    'apiKey': os.environ.get('BITGET_API_KEY'),
    'secret': os.environ.get('BITGET_SECRET_KEY'),
    'password': os.environ.get('BITGET_PASSPHRASE'),
    'enableRateLimit': True,
})

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    # 트레이딩뷰에서 보낸 신호대로 주문
    symbol = data.get('symbol', 'BTC/USDT')
    side = data.get('side') # 'buy' 또는 'sell'
    
    try:
        # 시장가 매수 주문
        order = exchange.create_market_order(symbol, side, amount=0.001)
        return jsonify({"status": "success", "order": order}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from binance import Client, ThreadedWebsocketManager
import time
import pandas as pd

api_key = "AbdA9V5CxGWEpFPFG8hbcYevMrOnpOORxa54QbZmiZkfaAwthmunpYskAnd5gYRV"
secret_key = "oMy0kwkxPBsl1Z4pey8pdcWLPeah5ASIrXugAT8UO99dVZ34WnymQmKj4Yci5QDe8c"

client = Client(api_key, secret_key)
klines = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, limit=100)

cols = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
        'quote_asset_volume', 'trades', 'taker_buy_base', 'taker_buy_quote', 'ignore']
df = pd.DataFrame(klines, columns=cols)
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df['close'] = df['close'].astype(float)

price = df['close'].iloc[-1]

client = Client(api_key, secret_key)
twm = ThreadedWebsocketManager(api_key=api_key, api_secret=secret_key)
twm.start()

real_time_price = None

def handle_socket_message(msg):
    if msg['e'] != 'kline':
        return

    candle = msg['k']
    is_closed = candle['x']
    close_price = candle['c']

    if is_closed:
        global real_time_price
        real_time_price = float(close_price)

twm.start_kline_socket(callback=handle_socket_message, symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1SECOND)

if __name__ == '__main__':
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        twm.stop()
        print("WebSocket stopped")
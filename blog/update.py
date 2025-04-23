from binance.client import Client
from binance import BinanceSocketManager
from binance import AsyncClient
import asyncio
from . import utils
from django.conf import settings
import numpy as np
import functools


scaler = utils.scaler


data_buffer = []

async def handle_socket(msg):
    candle = msg['k']
    if candle['x']:
        close_price = float(candle['c'])
        data_buffer.append(close_price)
        print(f"Harga diterima: {close_price}, Panjang buffer: {len(data_buffer)}")
        if len(data_buffer) > 60:
            data_buffer.pop(0)
        if len(data_buffer) == 60:
            print("Buffer mencapai 60, memanggil predict()")
            predict()
        
        global real_time_price
        real_time_price = close_price 
        print(f"Harga real-time: {real_time_price}")
    
def predict():
    """
    Sinkron: dipanggil scheduler tiap 60 menit
    """
    if len(data_buffer) < 60:
        return
    import numpy as np
    last_60 = np.array(data_buffer[-60:]).reshape(-1,1)
    scaled = scaler.transform(last_60)
    x_input = scaled.reshape(1,60,1)
    raw = utils.model.predict(x_input)
    global predicted_price
    predicted_price = float(scaler.inverse_transform(raw)[0][0])
    print(f"[Scheduler] Harga prediksi baru: {predicted_price}")

async def main():
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)
    socket = bm.kline_socket('BTCUSDT', interval=AsyncClient.KLINE_INTERVAL_1SECOND)
    msg = await socket.recv()
    await handle_socket(msg)
    # await asyncio.sleep(60)
    

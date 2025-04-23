import pandas as pd
import numpy as np
from . import get
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from binance import Client

data = get.df
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data[['close']])
client = get.client

seq_length = 60
available_len = len(scaled_data)
seq_length = seq_length if available_len >= seq_length else available_len - 1

X, y = [], []

# Ensure we have enough data to create at least one sequence
if len(scaled_data) > seq_length:
    for i in range(seq_length, len(scaled_data)):
        X.append(scaled_data[i - seq_length:i, 0])
        y.append(scaled_data[i, 0])

x = np.array(X)
y = np.array(y)

print(f"Shape of X: {np.array(X).shape if X else 'Empty'}")
print(f"Shape of x before reshape: {x.shape}")

# Reshape x only if it has at least one sequence
if x.ndim == 2 and x.shape[1] == seq_length:
    x = x.reshape((x.shape[0], x.shape[1], 1))
elif x.size > 0 and x.ndim == 1:
    # Handle the case where only one sequence was created
    x = x.reshape((1, x.shape[0], 1))
else:
    print(f"Warning: Input data x has unexpected shape: {x.shape}. Setting to empty.")
    x = np.empty((0, seq_length, 1)) # Assign an empty array

print(f"Shape of x after reshape attempts: {x.shape}")

# ... rest of your code ...

model = Sequential()
model.add(LSTM(units=60, return_sequences=True, input_shape=(x.shape[1], 1) if x.ndim == 3 and x.shape[1] > 0 else (seq_length, 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=60))
model.add(Dropout(0.2))
model.add(Dense(units=1))  # Output: prediksi harga close berikutnya

# ====== 8. Compile & Training Model ======
model.compile(optimizer='adam', loss='mean_squared_error')
if x.ndim == 3 and x.shape[0] > 0:
    model.fit(x, y, epochs=50, batch_size=32)
else:
    print("Warning: Skipping model training due to insufficient or incorrectly shaped data.")

# ====== 9. Prediksi Harga Selanjutnya ======
latest_data = client.get_klines(
    symbol='BTCUSDT',
    interval=Client.KLINE_INTERVAL_1MINUTE,
    limit=60
)
latest_close = np.array([float(k[4]) for k in latest_data]).reshape(-1, 1)
scaled_latest = scaler.transform(latest_close)
x_input = scaled_latest[-seq_length:].reshape((1, seq_length, 1))

# Make prediction only if the model has been trained and x has the correct shape
if x.ndim == 3 and x.shape[0] > 0:
    predicted_price = model.predict(x_input)
    predicted_price = scaler.inverse_transform(predicted_price)[0][0]
    print(f"Predicted Price: {predicted_price}")
else:
    print("Warning: Model not trained or insufficient training data, cannot make prediction.")
    predicted_price = None # Or some other default value

# return predicted_price
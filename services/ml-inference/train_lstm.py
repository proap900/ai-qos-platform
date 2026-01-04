"""
LSTM Training Script for Network QoS Prediction
------------------------------------------------
Generates synthetic network traffic data,
trains an LSTM model, and saves artifacts for inference service.
"""

import os
import numpy as np
import pandas as pd
import joblib

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam

# -----------------------------
# Configuration
# -----------------------------
TIME_STEPS = 10000
SEQ_LEN = 10
FEATURES = ["packet_rate", "bandwidth_util", "rtt_variance"]
TARGET = "latency"
MODEL_DIR = "model"
DATA_DIR = "data"

np.random.seed(42)

# -----------------------------
# Directory Setup
# -----------------------------
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# -----------------------------
# Data Generation
# -----------------------------
packet_rate = 1000 + 300 * np.sin(np.linspace(0, 50, TIME_STEPS))
bandwidth_util = 50 + 20 * np.sin(np.linspace(0, 20, TIME_STEPS))
rtt_variance = 5 + np.random.normal(0, 1, TIME_STEPS)

packet_rate += np.random.normal(0, 50, TIME_STEPS)
bandwidth_util += np.random.normal(0, 5, TIME_STEPS)

latency = (
    20
    + 0.02 * packet_rate
    + 0.5 * bandwidth_util
    + 2 * rtt_variance
    + np.random.normal(0, 5, TIME_STEPS)
)

data = pd.DataFrame({
    "packet_rate": packet_rate,
    "bandwidth_util": bandwidth_util,
    "rtt_variance": rtt_variance,
    "latency": latency
})

data_path = os.path.join(DATA_DIR, "synthetic_qos_data.csv")
data.to_csv(data_path, index=False)

print(f"[INFO] Dataset saved to {data_path}")

# -----------------------------
# Data Scaling
# -----------------------------
scaler = MinMaxScaler()
scaled = scaler.fit_transform(data)

# -----------------------------
# Sequence Preparation
# -----------------------------
X, y = [], []

for i in range(len(scaled) - SEQ_LEN):
    X.append(scaled[i:i + SEQ_LEN, :-1])
    y.append(scaled[i + SEQ_LEN, -1])

X = np.array(X)
y = np.array(y)

print("[INFO] Input shape:", X.shape)
print("[INFO] Output shape:", y.shape)

# -----------------------------
# Model Definition
# -----------------------------
model = Sequential([
    LSTM(50, input_shape=(SEQ_LEN, len(FEATURES))),
    Dense(1)
])

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss="mse"
)

# -----------------------------
# Model Training
# -----------------------------
model.fit(
    X,
    y,
    epochs=30,
    batch_size=64,
    validation_split=0.2,
    verbose=1
)

# -----------------------------
# Save Artifacts
# -----------------------------
model.save(os.path.join(MODEL_DIR, "lstm_qos_model.keras"))
joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.save"))

print("[SUCCESS] Model and scaler saved.")

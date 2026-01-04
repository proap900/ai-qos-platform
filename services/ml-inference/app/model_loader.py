import joblib
import numpy as np
from tensorflow.keras.models import load_model

MODEL_PATH = "model/lstm_qos_model.keras"
SCALER_PATH = "model/scaler.save"

model = None
scaler = None

def load_artifacts():
    global model, scaler
    model = load_model(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

def predict_latency(packet_rate, bandwidth_util, rtt_variance):
    # Build feature array
    X = np.column_stack([
        packet_rate,
        bandwidth_util,
        rtt_variance
    ])

    # Add dummy latency column to satisfy scaler (4 features)
    dummy_latency = np.zeros((X.shape[0], 1))
    X_with_dummy = np.hstack([X, dummy_latency])

    # Scale using trained scaler
    X_scaled = scaler.transform(X_with_dummy)

    # Remove dummy column after scaling
    X_scaled = X_scaled[:, :3]

    # Reshape for LSTM: (1, timesteps, features)
    X_scaled = X_scaled.reshape(1, X_scaled.shape[0], X_scaled.shape[1])

    prediction = model.predict(X_scaled, verbose=0)
    return float(prediction[0][0])

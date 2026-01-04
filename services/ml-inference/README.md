# ML Inference Service – QoS Prediction

This module trains an LSTM-based model to predict short-term
network latency (QoS) based on recent traffic metrics.

## Features Used
- Packet rate
- Bandwidth utilization
- RTT variance

## Output
- Predicted latency for next time interval

## Artifacts
- Trained LSTM model (`model/lstm_qos_model`)
- Feature scaler (`model/scaler.save`)

## Usage
```bash
source venv/bin/activate
python3 train_lstm.py

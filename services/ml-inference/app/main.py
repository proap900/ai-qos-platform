import time
from fastapi import FastAPI, HTTPException

from app.schemas import QoSRequest, QoSResponse
from app.model_loader import load_artifacts, predict_latency
from app.metrics import record_request, get_metrics

app = FastAPI(title="ML QoS Inference Service")

@app.on_event("startup")
def startup_event():
    load_artifacts()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return get_metrics()

@app.post("/predict", response_model=QoSResponse)
def predict(request: QoSRequest):
    if not (len(request.packet_rate) ==
            len(request.bandwidth_util) ==
            len(request.rtt_variance)):
        raise HTTPException(
            status_code=400,
            detail="Input feature lengths must match"
        )

    start = time.time()

    latency = predict_latency(
        request.packet_rate,
        request.bandwidth_util,
        request.rtt_variance
    )

    record_request(time.time() - start)

    return QoSResponse(predicted_latency=latency)

from fastapi import FastAPI, HTTPException
from app.schemas import QoSRequest, QoSResponse
from app.client import call_ml_service

app = FastAPI(title="QoS API Gateway")

@app.get("/health")
def health():
    return {"status": " ml gateway-ok"}

@app.post("/predict", response_model=QoSResponse)
def predict(request: QoSRequest):
    try:
        result = call_ml_service(request.dict())
        return QoSResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=str(e)
        )

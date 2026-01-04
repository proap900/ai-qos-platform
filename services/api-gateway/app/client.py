import requests

ML_SERVICE_URL = "http://ml-inference:8001"

def call_ml_service(payload: dict):
    response = requests.post(
        f"{ML_SERVICE_URL}/predict",
        json=payload,
        timeout=5
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"ML service error: {response.text}"
        )

    return response.json()

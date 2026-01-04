import time

request_count = 0
total_latency = 0.0

def record_request(latency):
    global request_count, total_latency
    request_count += 1
    total_latency += latency

def get_metrics():
    avg_latency = total_latency / request_count if request_count else 0
    return {
        "request_count": request_count,
        "average_inference_time_ms": round(avg_latency * 1000, 2)
    }

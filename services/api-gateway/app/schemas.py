from pydantic import BaseModel
from typing import List

class QoSRequest(BaseModel):
    packet_rate: List[float]
    bandwidth_util: List[float]
    rtt_variance: List[float]

class QoSResponse(BaseModel):
    predicted_latency: float

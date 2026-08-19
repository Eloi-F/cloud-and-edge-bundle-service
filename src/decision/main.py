import uvicorn
import os

from fastapi import FastAPI
from app.api.schemas import DecisionRequest, DecisionResponse

from app.core.speed_logic import calculate_speed
from odrl.pep.enforcer import enforce_odrl_policy

app = FastAPI()


@app.post("/decision", response_model=DecisionResponse)
def decision_endpoint(data: DecisionRequest):
    enforce_odrl_policy(data.metadata)

    speed = calculate_speed(data.front, data.state)
    return DecisionResponse(speed=speed)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8002)),
        reload=True,
    )

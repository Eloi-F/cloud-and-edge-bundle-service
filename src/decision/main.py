import uvicorn

from app.core.config import PORT

from fastapi import FastAPI, HTTPException
from app.api.schemas import DecisionRequest, DecisionResponse

from app.core.speed_logic import calculate_speed
from odrl.odrl_eval import ODRLEvaluator

app = FastAPI()

evaluator = ODRLEvaluator("./policies")


@app.post("/decision", response_model=DecisionResponse)
def read_root(data: DecisionRequest):
    """
    POST endpoint returning speed instruction based on distance to obstacle and cliff state.
    """
    if not evaluator.evaluate_and_enforce(data.metadata):
        raise HTTPException(
            status_code=401,
            detail="Forbidden by the data usage policy (ODRL).",
        )
    speed = calculate_speed(data.front, data.state)
    return DecisionResponse(speed=speed)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)

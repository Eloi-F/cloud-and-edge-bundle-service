import uvicorn
import os
import sys
import logging
from pathlib import Path
from fastapi import FastAPI

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.models.schemas import DecisionRequest, DecisionResponse, TrainingData
from src.decision.app.core.speed_logic import calculate_speed
from src.http_client import post_json
from src.logging_config.logging_config import setup_logging


logger = logging.getLogger(__name__)
setup_logging()
app = FastAPI()

STORAGE_URL = os.getenv("STORAGE_URL", "http://localhost:8004/storage")


@app.post("/decision", response_model=DecisionResponse)
def decision_endpoint(input_request: DecisionRequest):
    """
    Decision endpoint. Return speed value
    based on objects detected and distance
    between them and the car.

    :param input_request:
    :return:
    """
    logger.info("Received new request on /decision endpoint.")

    if not input_request.sensors:
        logger.error("Sensors are empty, can't evaluate the speed.")
        return DecisionResponse(speed=0)

    speed = calculate_speed(input_request.sensors.front, input_request.sensors.state)

    storage_request = TrainingData(
        bundle_id=input_request.bundle_id,
        image=input_request.image,
        detections=input_request.detections,
        speed=speed,
    )

    post_json(STORAGE_URL, storage_request)

    logger.debug("Sending back DecisionResponse(speed=%s)", speed)
    return DecisionResponse(speed=speed)


if __name__ == "__main__":
    uvicorn.run(
        "src.decision.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8002)),
        reload=True,
    )

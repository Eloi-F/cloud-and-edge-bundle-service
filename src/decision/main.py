import uvicorn
import os
import sys
import logging_config
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.models.schemas import DecisionRequest, DecisionResponse, TrainingData, Detection
from src.decision.app.core.speed_logic import calculate_speed
from src.odrl.pep.enforcer import verify_permissions, enforce_duties
from src.odrl.odrl_eval import ODRLEvaluator
from src.logging_config.logging_config import setup_logging



evaluator = ODRLEvaluator("./src/decision/policies")
logger = logging_config.getLogger(__name__)
setup_logging()
app = FastAPI()


def get_current_date() -> str:
    """Return the current date/time in ISO format (YYYY-MM-DDTHH:MM:SS)."""
    return datetime.now().isoformat(timespec="seconds")


def build_storage_request(
        bundle_id: str,
        img: str,
        detections: list[Detection],
        speed: float | None
) -> TrainingData :
    """Build TrainingData object with detections to send to /storage endpoint."""

    logger.debug("Building TrainingData object to send to /storage endpoint.")
    return TrainingData(
        bundle_id=bundle_id,
        metadata={
            "http://www.w3.org/ns/odrl/2/dateTime": get_current_date(),
            "http://www.w3.org/ns/odrl/2/Party": "urn:capacity:storage",
            "http://www.w3.org/ns/odrl/2/Action": "urn:action:store",
            "http://www.w3.org/ns/odrl/2/Asset": "urn:data:input"
        },
        image=img,
        detections=detections,
        speed=speed
    )

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
    history, pending_duties = verify_permissions(
        evaluator, input_request.bundle_id, input_request.metadata
    )
    logger.debug("Pending duties: %s", pending_duties)

    if not input_request.sensors:
        logger.error("Sensors are empty, can't evaluate the speed.")
        return DecisionResponse(speed=0)

    speed = calculate_speed(input_request.sensors.front, input_request.sensors.state)

    request = build_storage_request(
        input_request.bundle_id,
        input_request.image,
        input_request.detections,
        speed
    )

    enforce_duties(
        evaluator,
        bundle_id=input_request.bundle_id,
        history=history,
        duties=pending_duties,
        payload=request,
    )

    logger.debug("Sending back DecisionResponse(speed=%s)",speed)
    return DecisionResponse(speed=speed)


if __name__ == "__main__":
    uvicorn.run(
        "src.decision.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8002)),
        reload=True,
    )

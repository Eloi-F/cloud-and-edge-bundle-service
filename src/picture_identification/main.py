import logging
import uvicorn
import os
import sys
from pathlib import Path
from fastapi import FastAPI

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.models.schemas import (
    IdentificationRequest,
    IdentificationResponse,
    DecisionRequest,
    DecisionResponse,
    Detection,
    TrainingData,
)
from src.logging_config.logging_config import setup_logging
from src.picture_identification.app.core.identification_logic import identify_objects
from src.http_client import post_json


setup_logging()
app = FastAPI()

logger = logging.getLogger(__name__)

STORAGE_URL = os.getenv("STORAGE_URL", "http://localhost:8004/storage")
DECISION_URL = os.getenv("DECISION_URL", "http://localhost:8002/decision")


def parse_bundle_id(bundle_id: str) -> str:
    """Return parsed bundle id."""
    return bundle_id.rsplit(":", 1)[-1]


def build_identification_response(
    img: str,
    detections: list[Detection],
) -> IdentificationResponse:
    """Build IdentificationResponse object with detections to send back."""

    logger.debug("Building IdentificationResponse to send back.")
    return IdentificationResponse(image=img, detections=detections)


@app.post("/identification")
def identification(input_request: IdentificationRequest):
    """
    Identification endpoint. Performs AI recognition on
    input image to detect obstacles on road.

    :param input_request:
    :return:
    """

    logger.info("Received new request on /identification endpoint.")

    # Perform AI detection on image
    detections = identify_objects(input_request.image)

    # Bundle 1 -> Storage request + Identification response
    if parse_bundle_id(input_request.bundle_id) == "bundle1":
        storage_request = TrainingData(
            bundle_id=input_request.bundle_id,
            image=input_request.image,
            detections=detections,
            speed=None,
        )
        post_json(STORAGE_URL, storage_request)
        return build_identification_response(input_request.image, detections)

    # Bundle 2 -> Decision request + Decision response
    else:
        decision_request = DecisionRequest(
            bundle_id=input_request.bundle_id,
            image=input_request.image,
            detections=detections,
            sensors=input_request.sensors,
        )
        decision_resp = post_json(DECISION_URL, decision_request)
        return DecisionResponse(speed=decision_resp.get("speed", 0))


if __name__ == "__main__":
    uvicorn.run(
        "src.picture_identification.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
    )

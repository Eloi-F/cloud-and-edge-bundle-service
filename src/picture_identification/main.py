from email.mime import image

import logging_config
import uvicorn
import os
import sys
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, HTTPException

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.models.schemas import (
    IdentificationRequest,
    IdentificationResponse,
    DecisionRequest,
    DecisionResponse,
    Detection,
    TrainingData,
    Sensors
)
from src.logging_config.logging_config import setup_logging
from src.picture_identification.app.core.identification_logic import identify_objects
from src.odrl.pep.enforcer import verify_permissions, enforce_duties
from src.odrl.odrl_eval import ODRLEvaluator


setup_logging()
app = FastAPI()

logger = logging_config.getLogger(__name__)
evaluator = ODRLEvaluator("./src/picture_identification/policies")
BUNDLE_PATH = "urn:policy:bundle"


def parse_bundle_id(bundle_id: str) -> str :
    """Return parsed bundle id."""
    return bundle_id.rsplit(":",1)[-1]


def get_current_date() -> str:
    """Return the current date/time in ISO format (YYYY-MM-DDTHH:MM:SS)."""
    return datetime.now().isoformat(timespec="seconds")


def build_identification_response(
        img: str,
        detections: list[Detection]
) -> IdentificationResponse :
    """Build IdentificationResponse object with detections to send back."""

    logger.debug("Building IdentificationResponse to send back.")
    return IdentificationResponse(
        image=img,
        detections=detections
    )

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

def build_decision_request(
        bundle_id: str,
        img: str,
        detections: list[Detection],
        sensors: Sensors | None
) -> DecisionRequest :
    """Build DecisionRequest object with detections and sensors to send to /decision endpoint."""

    logger.debug("Building TrainingData object to send to /storage endpoint.")
    return DecisionRequest(
        bundle_id=bundle_id,
        metadata={
            "http://www.w3.org/ns/odrl/2/dateTime": get_current_date(),
            "http://www.w3.org/ns/odrl/2/Party": "urn:capacity:decision",
            "http://www.w3.org/ns/odrl/2/Action": "urn:action:compute-decision",
            "http://www.w3.org/ns/odrl/2/Asset": "urn:data:input"
        },
        image=img,
        detections=detections,
        sensors=sensors
    )


@app.post("/identification")
def identification(input_request: IdentificationRequest):
    """
    Identification endpoint. Performs AI recognition on
    input image to detect obstacles on road.

    :param input_request:
    :return:
    """

    logger.info("Received new request on /identification endpoint.")

    history, pending_duties = verify_permissions(
        evaluator, input_request.bundle_id, input_request.metadata
    )
    logger.debug("Pending duties: %s", pending_duties)

    # Perform AI detection on image
    detections = identify_objects(input_request.image)

    # Bundle 1 -> Storage request + Identification response
    if parse_bundle_id(input_request.bundle_id) == "bundle1":
        enforce_duties(
            evaluator,
            bundle_id=input_request.bundle_id,
            history=history,
            duties=pending_duties,
            payload=build_storage_request(
                input_request.bundle_id,
                input_request.image,
                detections,
                None
            )
        )
        return build_identification_response(input_request.image,detections)

    # Bundle 2 -> Decision request + Decision response
    else :
        result = enforce_duties(
            evaluator,
            bundle_id=input_request.bundle_id,
            history=history,
            duties=pending_duties,
            payload=build_decision_request(
                input_request.bundle_id,
                input_request.image,
                detections,
                input_request.sensors
            )
        )
        decision_resp = result.get("urn:capacity:decision", {})
        return DecisionResponse(speed=decision_resp.get("speed", 0))


if __name__ == "__main__":
    uvicorn.run(
        "src.picture_identification.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
    )

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
)

from src.picture_identification.app.core.identification_logic import identify_objects
from src.odrl.pep.enforcer import verify_permissions, enforce_duties

import logging
from src.logging.logging_config import setup_logging

logger = logging.getLogger(__name__)

from src.odrl.odrl_eval import ODRLEvaluator

evaluator = ODRLEvaluator("./src/picture_identification/policies")

setup_logging()
app = FastAPI()


@app.post("/identification")
def identification(data: IdentificationRequest):
    logger.info("Received new request on /identification endpoint.")
    history, pending_duties = verify_permissions(
        evaluator, data.bundle_id, data.metadata
    )
    logger.debug(f"Pending duties: {pending_duties}")

    detections = identify_objects(data.image)

    decision_req = DecisionRequest(
        bundle_id=data.bundle_id,
        metadata=data.metadata,
        image=data.image,
        detections=detections,
        sensors=data.sensors,
    )

    result = enforce_duties(
        evaluator,
        bundle_id=data.bundle_id,
        history=history,
        duties=pending_duties,
        payload=decision_req,
    )

    if data.bundle_id == "urn:policy:bundle:bundle1":
        return IdentificationResponse(image=data.image, detections=detections)

    elif data.bundle_id == "urn:policy:bundle:bundle2":
        decision_resp = result.get("urn:capacity:decision", {})
        return DecisionResponse(speed=decision_resp.get("speed", 0))


if __name__ == "__main__":
    uvicorn.run(
        "src.picture_identification.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
    )

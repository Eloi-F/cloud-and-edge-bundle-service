import uvicorn
import os

from fastapi import FastAPI

from src.models.schemas import (
    IdentificationRequest,
    IdentificationResponse,
    SensoryIdentificationResponse,
)

from src.picture_identification.app.core.identification_logic import identify_objects
from src.odrl.pep.enforcer import verify_permissions, enforce_duties

import logging
from src.logging.logging_config import setup_logging

logger = logging.getLogger(__name__)

setup_logging()
app = FastAPI()


@app.post("/identification")
def identification(data: IdentificationRequest):
    logger.info("Received new request on /identification endpoint.")
    history, pending_duties = verify_permissions(data.bundle_id, data.metadata)
    logger.debug(f"Pending duties: {pending_duties}")

    detections = identify_objects(data.image)

    enforce_duties(history=history, duties=pending_duties, payload=dict(data))

    if data.sensors is not None:
        return SensoryIdentificationResponse(
            image=data.image,
            detections=detections,
            sensors=data.sensors,
        )
    return IdentificationResponse(image=data.image, detections=detections)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
    )

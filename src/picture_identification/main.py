import uvicorn
import os

from fastapi import FastAPI

from app.api.schemas import IdentificationRequest, IdentificationResponse
from app.core.identification_logic import identify_objects
from odrl.pep.enforcer import verify_permissions, enforce_duties

import logging
from src.logging.logging_config import setup_logging
logger = logging.getLogger(__name__)

setup_logging()
app = FastAPI()


@app.post("/identification", response_model=IdentificationResponse)
def identification(data: IdentificationRequest):
	logger.info("Received new request on /identification endpoint.")
	history, pending_duties = verify_permissions(data.bundle_id, data.metadata)
	logger.debug(f"Pending duties: {pending_duties}")

	detections = identify_objects(data.image)

	data.detections = IdentificationResponse(detections=detections, speed=0)
	speed = enforce_duties(history=history, duties=pending_duties, payload=data)

	return IdentificationResponse(detections=detections, speed=speed)


if __name__ == "__main__":
	uvicorn.run(
		"main:app",
		host="0.0.0.0",
		port=int(os.getenv("PORT", 8000)),
		reload=True,
	)

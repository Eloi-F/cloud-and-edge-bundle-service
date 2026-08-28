import uvicorn
import os

from fastapi import FastAPI
from app.api.schemas import DecisionRequest, DecisionResponse

from app.core.speed_logic import calculate_speed
from odrl.pep.enforcer import verify_permissions, enforce_duties

import logging
from src.logging.logging_config import setup_logging
logger = logging.getLogger(__name__)

setup_logging()
app = FastAPI()


@app.post("/decision", response_model=DecisionResponse)
def decision_endpoint(data: DecisionRequest):
	logger.info("Received new request on /decision endpoint.")
	history, pending_duties = verify_permissions(data.bundle_id, data.metadata)
	logger.debug(f"Pending duties: {pending_duties}")

	speed = calculate_speed(data.front, data.state)

	payload = {
		"image": DecisionRequest.image,
		"speed": speed,
		"detections": DecisionRequest.detections,
		"bundle_id": data.bundle_id,
	}

	enforce_duties(history=history, duties=pending_duties, payload=payload)

	return DecisionResponse(speed=speed)


if __name__ == "__main__":
	uvicorn.run(
		"main:app",
		host="0.0.0.0",
		port=int(os.getenv("PORT", 8002)),
		reload=True,
	)

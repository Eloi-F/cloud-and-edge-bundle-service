import os

from fastapi import FastAPI
import uvicorn

from app.api.schemas import ResizeRequest
from app.core.crop import crop_with_padding
from odrl.pep.enforcer import verify_permissions, enforce_duties

import logging
from src.logging.logging_config import setup_logging
logger = logging.getLogger(__name__)

setup_logging()
app = FastAPI()


@app.post("/resize")
async def resize_image(data: ResizeRequest):
	logger.info("Received new request on /resize_image endpoint.")
	history, pending_duties = verify_permissions(data.bundle_id, data.metadata)
	logger.debug(f"Pending duties: {pending_duties}")

	result = crop_with_padding(data.image)

	speed = enforce_duties(history=history, duties=pending_duties, payload=result)

	return speed


if __name__ == "__main__":
	uvicorn.run(
		"main:app",
		host="0.0.0.0",
		port=int(os.getenv("PORT", 8002)),
		reload=True,
	)

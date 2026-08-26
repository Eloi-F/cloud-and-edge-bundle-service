import uvicorn
import os

from fastapi import FastAPI
from app.api.schemas import StorageRequest, StorageResponse
from app.core.storage_logic import store_sample, create_storage

import logging
from logging_config import setup_logging

logger = logging.getLogger(__name__)

setup_logging()
create_storage()
app = FastAPI()


@app.post("/storage", response_model=StorageResponse)
def storage_endpoint(data: StorageRequest):
	"""
	Storage service endpoint. Stores image
	and associated detections in database.

	:param data:
	:return: bool
	"""
	logger.info("Received new storage request on /storage endpoint.")
	result = store_sample(
		data.image,
		data.speed,
		data.detection_list.detections
	)

	return StorageResponse(stored = result)


if __name__ == "__main__":
	uvicorn.run(
		"main:app",
		host="0.0.0.0",
		port=int(os.getenv("PORT", 8005)),
		reload=True,
	)

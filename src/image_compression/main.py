import os
import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.models.schemas import (
    IdentificationRequest,
    ImageResponse,
    SensoryImageResponse,
)

from src.image_compression.app.core.crop import crop_with_padding
from src.odrl.pep.enforcer import verify_permissions, enforce_duties

import logging
from src.logging.logging_config import setup_logging

from src.odrl.odrl_eval import ODRLEvaluator

evaluator = ODRLEvaluator("./src/image_compression/policies")

logger = logging.getLogger(__name__)

setup_logging()
app = FastAPI()


@app.post("/resize")
async def resize_image(data: IdentificationRequest):
    logger.info("Received new request on /resize_image endpoint.")
    history, pending_duties = verify_permissions(
        evaluator, data.bundle_id, data.metadata
    )
    logger.debug(f"Pending duties: {pending_duties}")

    result = crop_with_padding(data.image)

    enforce_duties(evaluator, history=history, duties=pending_duties, payload=result)

    if data.sensors is not None:
        return SensoryImageResponse(image=result["image"], sensors=data.sensors)
    return ImageResponse(image=result["image"])


if __name__ == "__main__":
    uvicorn.run(
        "src.image_compression.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8003)),
        reload=True,
    )

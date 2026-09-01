import os
import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.models.schemas import IdentificationRequest

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

    data.image = crop_with_padding(data.image)

    result = enforce_duties(
        evaluator,
        bundle_id=data.bundle_id,
        history=history,
        duties=pending_duties,
        payload=data,
    )

    identification_resp = result.get("urn:capacity:identification", {})

    if data.bundle_id == "urn:policy:bundle:bundle1":
        return identification_resp.get("detections")

    elif data.bundle_id == "urn:policy:bundle:bundle2":
        return identification_resp.get("speed")


if __name__ == "__main__":
    uvicorn.run(
        "src.image_compression.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8003)),
        reload=True,
    )

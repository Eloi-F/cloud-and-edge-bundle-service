import logging
import os
import sys
import uvicorn
from pathlib import Path
from fastapi import FastAPI

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.models.schemas import IdentificationRequest
from src.image_compression.app.core.crop import crop_with_padding
from src.http_client import post_json
from src.logging_config.logging_config import setup_logging


setup_logging()
app = FastAPI()

logger = logging.getLogger(__name__)

IDENTIFICATION_URL = os.getenv("IDENTIFICATION_URL", "http://localhost:8000/identification")


@app.post("/resize")
def resize_image(input_request: IdentificationRequest):
    """
    Resize endpoint. Facilitates identification method
    in bundles 1 and 2 by compressing input image given
    to Identification capacity.

    :param input_request:
    :return: detections         if bundle 1
             speed instruction  if bundle 2
    """

    logger.info("Received new request on /resize endpoint.")

    resized_request = IdentificationRequest(
        bundle_id=input_request.bundle_id,
        image=crop_with_padding(input_request.image),
        sensors=input_request.sensors,
    )

    identification_resp = post_json(IDENTIFICATION_URL, resized_request)

    if input_request.bundle_id == "urn:policy:bundle:bundle1":
        return identification_resp.get("detections")

    else:  # Bundle 2
        return identification_resp.get("speed")


if __name__ == "__main__":
    uvicorn.run(
        "src.image_compression.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8003)),
        reload=True,
    )

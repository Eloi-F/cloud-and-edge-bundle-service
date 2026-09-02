import logging
import os
import sys
import uvicorn
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, HTTPException

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.models.schemas import IdentificationRequest, Sensors
from src.image_compression.app.core.crop import crop_with_padding
from src.logging_config.logging_config import setup_logging
from src.odrl.pep.enforcer import verify_permissions, enforce_duties
from src.odrl.odrl_eval import ODRLEvaluator


setup_logging()
app = FastAPI()

evaluator = ODRLEvaluator("./src/image_compression/policies")
logger = logging.getLogger(__name__)
BUNDLE_PATH = "urn:policy:bundle"

def get_current_date() -> str:
    """Return the current date/time in ISO format (YYYY-MM-DDTHH:MM:SS)."""
    return datetime.now().isoformat(timespec="seconds")


def build_resized_identification_request(
        bundle_id: str,
        image: str,
        sensors: Sensors | None,
) -> IdentificationRequest :
    """Build IdentificationRequest object with resized image to send to /identification endpoint."""

    logger.debug("Building resized request.")
    return IdentificationRequest(
        bundle_id=bundle_id,
        metadata={
            "http://www.w3.org/ns/odrl/2/dateTime": get_current_date(),
            "http://www.w3.org/ns/odrl/2/Party": "urn:capacity:identification",
            "http://www.w3.org/ns/odrl/2/Action": "urn:action:compute-recognition",
            "http://www.w3.org/ns/odrl/2/Asset": "urn:data:input"
        },
        image=crop_with_padding(image),
        sensors=sensors
    )


@app.post("/resize")
async def resize_image(input_request: IdentificationRequest):
    """
    Resize endpoint. Facilitates identification method
    in bundles 1 and 2 by compressing input image given
    to Identification capacity.

    :param input_request:
    :return: detections         if bundle 1
             speed instruction  if bundle 2
    """

    logger.info("Received new request on /resize endpoint.")

    history, pending_duties = verify_permissions(
        evaluator, input_request.bundle_id, input_request.metadata
    )
    logger.debug("Pending duties: %s", pending_duties)

    resized_request = build_resized_identification_request(
        input_request.bundle_id,
        input_request.image,
        input_request.sensors
    )

    result = enforce_duties(
        evaluator,
        bundle_id=input_request.bundle_id,
        history=history,
        duties=pending_duties,
        payload=resized_request,
    )

    identification_resp = result.get("urn:capacity:identification", {})

    if input_request.bundle_id == "urn:policy:bundle:bundle1":
        return identification_resp.get("detections")

    else: # Bundle 2
        return identification_resp.get("speed")


if __name__ == "__main__":
    uvicorn.run(
        "src.image_compression.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8003)),
        reload=True,
    )

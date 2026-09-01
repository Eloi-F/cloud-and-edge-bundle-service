import uvicorn
import os
import sys
from pathlib import Path

from fastapi import FastAPI

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.models.schemas import TrainingData
from src.data_storage.app.core.storage_logic import store_sample, create_storage

from src.odrl.pep.enforcer import verify_permissions, enforce_duties

import logging
from src.logging.logging_config import setup_logging

from src.odrl.odrl_eval import ODRLEvaluator

evaluator = ODRLEvaluator("./src/data_storage/policies")

logger = logging.getLogger(__name__)

setup_logging()
create_storage()
app = FastAPI()


@app.post("/storage")
def storage_endpoint(data: TrainingData):
    """
    Storage service endpoint. Stores image
    and associated detections in database.

    :return: bool
    """
    logger.info("Received new request on /storage endpoint.")
    history, pending_duties = verify_permissions(
        evaluator, data.bundle_id, data.metadata
    )
    logger.debug(f"Pending duties: {pending_duties}")

    result = store_sample(
        image=data.image,
        speed=data.speed,
        detections=data.detections,
    )

    enforce_duties(evaluator, history=history, duties=pending_duties, payload={})

    logger.info(f"Sending back StorageResponse(stored={result})")
    return result


if __name__ == "__main__":
    uvicorn.run(
        "src.data_storage.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8005)),
        reload=True,
    )

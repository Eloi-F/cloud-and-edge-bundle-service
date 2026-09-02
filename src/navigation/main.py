import os
import logging
import sys
import uvicorn
from pathlib import Path
from fastapi import FastAPI

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.models.schemas import TrajectoryRequest
from src.logging_config.logging_config import setup_logging

logger = logging.getLogger(__name__)
setup_logging()
app = FastAPI()


@app.post("/trajectory_planning")
async def navigation_endpoint(data: TrajectoryRequest):
    """
    Incomplete navigation endpoint. Performs
    shortest path between source and dest.

    :param data:
    :return:
    """

    logger.info("Received new request on /navigation endpoint.")

    return {"success": "True"}


if __name__ == "__main__":
    uvicorn.run(
        "src.navigation.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8001)),
        reload=True,
    )

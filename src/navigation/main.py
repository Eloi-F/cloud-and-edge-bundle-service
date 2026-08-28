import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.schemas import TrajectoryRequest
from app.core.trajectory_logic import build_trajectory_map

from odrl.pep.enforcer import verify_permissions, enforce_duties

import logging
from src.logging.logging_config import setup_logging
logger = logging.getLogger(__name__)

setup_logging()
app = FastAPI()


@app.post("/trajectory_planning")
async def navigation_endpoint(data: TrajectoryRequest):
    """Handle trajectory planning requests."""

    logger.info("Received new request on /navigation endpoint.")
    history, pending_duties = verify_permissions(data.bundle_id, data.metadata)
    logger.debug(f"Pending duties: {pending_duties}")

    folium_map = build_trajectory_map(data.start_address, data.destination_address)
    map_file = "map.html"
    folium_map.save(map_file)

    enforce_duties(history=history, duties=pending_duties, payload={})

    return FileResponse(map_file, media_type="file", filename=map_file)


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8001)), reload=True
    )

import os
import sys
from pathlib import Path
import uvicorn
from fastapi import FastAPI

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# from fastapi.responses import FileResponse

from src.models.schemas import TrajectoryRequest

# from src.navigation.app.core.trajectory_logic import build_trajectory_map

from src.odrl.pep.enforcer import verify_permissions

# from src.odrl.pep.enforcer import enforce_duties

import logging
from src.logging.logging_config import setup_logging

from src.odrl.odrl_eval import ODRLEvaluator

evaluator = ODRLEvaluator("./src/navigation/policies")

logger = logging.getLogger(__name__)

setup_logging()
app = FastAPI()


@app.post("/trajectory_planning")
async def navigation_endpoint(data: TrajectoryRequest):
    """Handle trajectory planning requests."""

    logger.info("Received new request on /navigation endpoint.")
    history, pending_duties = verify_permissions(
        evaluator, data.bundle_id, data.metadata
    )
    logger.debug(f"Pending duties: {pending_duties}")

    return {"success": "True"}

    # folium_map = build_trajectory_map(data.start_address, data.destination_address)
    # map_file = "map.html"
    # folium_map.save(map_file)
    #
    # enforce_duties(evaluator, history=history, duties=pending_duties, payload={})
    #
    # logger.info("Sending back FileResponse.")
    # return FileResponse(map_file, media_type="file", filename=map_file)


if __name__ == "__main__":
    uvicorn.run(
        "src.navigation.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8001)),
        reload=True,
    )

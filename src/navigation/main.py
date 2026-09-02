import os
import logging
import sys
import uvicorn
from pathlib import Path
from fastapi import FastAPI
# from fastapi.responses import FileResponse

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.models.schemas import TrajectoryRequest
# from src.navigation.app.core.trajectory_logic import build_trajectory_map
from src.odrl.pep.enforcer import verify_permissions
# from src.odrl.pep.enforcer import enforce_duties
from src.odrl.odrl_eval import ODRLEvaluator
from src.logging_config.logging_config import setup_logging

evaluator = ODRLEvaluator("./src/navigation/policies")
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
    history, pending_duties = verify_permissions(
        evaluator, data.bundle_id, data.metadata
    )
    logger.debug("Building TrainingData object to send to /storage endpoint.")

    # folium_map = build_trajectory_map(data.start_address, data.destination_address)
    # map_file = "map.html"
    # folium_map.save(map_file)
    #
    # enforce_duties(evaluator, history=history, duties=pending_duties, payload={})
    #
    # logger.info("Sending back FileResponse.")
    # return FileResponse(map_file, media_type="file", filename=map_file)

    return {"success": "True"}


if __name__ == "__main__":
    uvicorn.run(
        "src.navigation.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8001)),
        reload=True,
    )

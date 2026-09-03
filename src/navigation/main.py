import os
import logging
import sys
import uvicorn
from pathlib import Path
from fastapi import FastAPI
from osmnx import graph

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.commons.schemas import TrajectoryRequest, TrajectoryResponse
from src.navigation.app.core.trajectory_logic import compute_shortest_path
from src.odrl.pep.enforcer import verify_permissions, enforce_duties
from src.odrl.odrl_eval import ODRLEvaluator
from src.logging_config.logging_config import setup_logging

evaluator = ODRLEvaluator("./src/navigation/policies")
logger = logging.getLogger(__name__)
setup_logging()
app = FastAPI()

logger.debug("Loading Toulouse map...")
toulouse_map = graph.graph_from_address(
    "Place du Capitole, 31000 Toulouse",
    2000,
    dist_type="network",
    network_type="all"
)
logger.debug("Successfully downloaded Toulouse map. 5km around Place du Capitole.")


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

    route = compute_shortest_path(
        toulouse_map,
        data.start_address,
        data.destination_address
    )

    enforce_duties(
        evaluator,
        bundle_id=data.bundle_id,
        history=history,
        duties=pending_duties,
        payload={}
    )

    logger.debug("Sending back shortest path.")
    logger.debug("route = %s",route)

    return TrajectoryResponse(route=route)


if __name__ == "__main__":
    uvicorn.run(
        "src.navigation.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8001)),
        reload=True,
    )

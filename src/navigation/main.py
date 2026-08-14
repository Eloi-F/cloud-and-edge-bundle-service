import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from app.core.config import PORT
from app.api.schemas import TrajectoryRequest

from app.core.trajectory_logic import build_trajectory_map
from odrl.odrl_eval import ODRLEvaluator

app = FastAPI()

# Initialize evaluator at startup (loading the unique graph)
evaluator = ODRLEvaluator("./policies")


@app.post("/trajectory_planning")
async def navigation_endpoint(data: TrajectoryRequest):
    """
    Main endpoint: Trajectory planning.
    """

    # 1. ODRL access control
    if not evaluator.evaluate_and_enforce(data.metadata):
        raise HTTPException(
            status_code=401,
            detail="Forbidden by the data usage policy (ODRL).",
        )

    folium_map = build_trajectory_map(
        data.start_address,
        data.destination_address,
    )

    map_file = "map.html"
    folium_map.save(map_file)

    return FileResponse(
        map_file,
        media_type="text/html",
        filename=map_file,
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)

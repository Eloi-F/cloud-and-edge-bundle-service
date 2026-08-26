import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.schemas import TrajectoryRequest
from app.core.trajectory_logic import build_trajectory_map

from odrl.pep.enforcer import verify_permissions, enforce_duties

app = FastAPI()


@app.post("/trajectory_planning")
async def navigation_endpoint(data: TrajectoryRequest):
    """Handle trajectory planning requests."""

    history, pending_duties = verify_permissions(data.bundle_id, data.metadata)

    folium_map = build_trajectory_map(data.start_address, data.destination_address)
    map_file = "map.html"
    folium_map.save(map_file)

    enforce_duties(history=history, duties=pending_duties, payload=folium_map)

    return FileResponse(map_file, media_type="file", filename=map_file)


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8001)), reload=True
    )

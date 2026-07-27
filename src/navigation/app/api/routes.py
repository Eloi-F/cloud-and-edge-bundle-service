from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.api.schemas import TrajectoryRequest
from app.core.trajectory_logic import build_trajectory_map

router = APIRouter()


@router.post("/trajectory_planning")
def trajectory_planning(data: TrajectoryRequest):
    """
    Generate the shortest itinerary and return it as an HTML map.
    """

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

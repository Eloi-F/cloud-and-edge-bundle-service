from fastapi import APIRouter
from app.api.schemas import DecisionRequest, DecisionResponse
from app.core.speed_logic import calculate_speed

router = APIRouter()


@router.post("/decision", response_model=DecisionResponse)
def read_root(data: DecisionRequest):
    """
    POST endpoint returning speed instruction based on distance to obstacle and cliff state.
    """
    speed = calculate_speed(data.front, data.state)
    return DecisionResponse(speed=speed)

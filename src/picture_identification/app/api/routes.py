from fastapi import APIRouter

from app.api.schemas import IdentificationRequest, IdentificationResponse
from app.core.identification_logic import identify_objects

router = APIRouter()


@router.post("/identification", response_model=IdentificationResponse)
def identification(data: IdentificationRequest):
    detections = identify_objects(data.image)

    return IdentificationResponse(detections=detections)

from pydantic import BaseModel


class DecisionRequest(BaseModel):
    front: float
    state: bool
    image: str
    detections: IdentificationResponse
    metadata: dict


class BoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int


class Detection(BaseModel):
    classId: str
    confidence: float
    box: BoundingBox


class IdentificationResponse(BaseModel):
    detections: list[Detection]


class DecisionResponse(BaseModel):
    speed: float

from pydantic import BaseModel


class DecisionRequest(BaseModel):
    bundle_id: str
    detections: IdentificationResponse
    front: float
    image: str
    metadata: dict
    state: bool


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

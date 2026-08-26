from pydantic import BaseModel


class IdentificationRequest(BaseModel):
    bundle_id: str
    detections: IdentificationResponse
    front: float
    image: str  # Base64-encoded image
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
    speed: float

from pydantic import BaseModel


class IdentificationRequest(BaseModel):
    image: str  # Base64-encoded image
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

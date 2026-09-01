from pydantic import BaseModel


class BoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int


class Detection(BaseModel):
    class_id: str
    confidence: float
    box: BoundingBox


class Sensors(BaseModel):
    front: float
    state: bool


class IdentificationRequest(BaseModel):
    bundle_id: str
    metadata: dict
    image: str
    sensors: Sensors | None = None


class DecisionRequest(BaseModel):
    bundle_id: str
    metadata: dict
    image: str
    detections: list[Detection]
    sensors: Sensors | None = None


class DecisionResponse(BaseModel):
    speed: float


class ImageResponse(BaseModel):
    image: str


class SensoryImageResponse(ImageResponse):
    sensors: Sensors


class IdentificationResponse(BaseModel):
    image: str
    detections: list[Detection]


class SensoryIdentificationResponse(IdentificationResponse):
    sensors: Sensors


class TrainingData(BaseModel):
    bundle_id: str
    metadata: dict
    image: str
    detections: list[Detection]
    speed: float | None = None


class TrajectoryRequest(BaseModel):
    bundle_id: str
    metadata: dict
    start_address: str
    destination_address: str

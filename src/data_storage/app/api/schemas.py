from pydantic import BaseModel


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


class StorageRequest(BaseModel):
	bundle_id: str
	image: str  # Base64-encoded image
	detection_list: IdentificationResponse
	speed: float | None = None


class StorageResponse(BaseModel):
	stored: bool

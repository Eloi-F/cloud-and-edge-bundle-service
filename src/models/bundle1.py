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

class IdentificationRequest(BaseModel):
	bundle_id: str
	metadata: dict
	img: str

class Detections(BaseModel):
	detections: list[Detection]

class TrainingData(BaseModel):
	bundle_id: str
	metadata: dict
	img_base64: str
	detections: Detections

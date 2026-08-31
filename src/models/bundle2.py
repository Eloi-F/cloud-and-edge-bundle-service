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

class Image(BaseModel):
	img_base64: str

class Sensors(BaseModel):
	speed: float
	state: bool

class IdentificationRequest(BaseModel):
	bundle_id: str
	metadata: dict
	img_base64: Image
	sensors: Sensors

class DecisionRequest(BaseModel):
	bundle_id: str
	metadata: dict
	id_request: IdentificationRequest
	detections: list[Detection]

class StorageRequest(BaseModel):
	bundle_id: str
	metadata: dict
	img_base64: Image
	detections: list[Detection]
	speed: float
from pydantic import BaseModel
from fastapi.responses import FileResponse


class TrajectoryRequest(BaseModel):
	bundle_id: str
	metadata: dict
	start_address: str
	destination_address: str

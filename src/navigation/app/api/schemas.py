from pydantic import BaseModel


class TrajectoryRequest(BaseModel):
    start_address: str
    destination_address: str
    metadata: dict
    bundle_id: str

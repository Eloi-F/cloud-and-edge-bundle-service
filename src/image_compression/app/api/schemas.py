from pydantic import BaseModel


class ResizeRequest(BaseModel):
    bundle_id: str
    front: float
    image: str
    metadata: dict
    state: bool

from pydantic import BaseModel


class DecisionRequest(BaseModel):
    front: float
    state: bool
    image: str
    metadata: dict


class DecisionResponse(BaseModel):
    speed: float

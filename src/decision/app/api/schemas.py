from pydantic import BaseModel


class DecisionRequest(BaseModel):
    front: float
    state: bool
    metadata: dict


class DecisionResponse(BaseModel):
    speed: float

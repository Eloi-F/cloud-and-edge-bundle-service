from pydantic import BaseModel


class DecisionRequest(BaseModel):
    front: float
    state: bool


class DecisionResponse(BaseModel):
    speed: float

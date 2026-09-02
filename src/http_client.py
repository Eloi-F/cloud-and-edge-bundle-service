import requests
from pydantic import BaseModel


def post_json(endpoint: str, payload: BaseModel) -> dict:
    """POST a Pydantic payload to an endpoint and return the parsed JSON response."""
    response = requests.post(endpoint, json=payload.model_dump(mode="json"), timeout=60)
    response.raise_for_status()
    return response.json()

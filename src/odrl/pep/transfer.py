from pydantic import BaseModel
import requests
import logging
from src.logging.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def delegate_to(endpoint: str, data: BaseModel):
    """Delegate a task to an endpoint and wait for its result."""
    logger.debug(f"Sending post request to {endpoint}.")
    response = requests.post(endpoint, json=data.model_dump(mode="json"))
    response.raise_for_status()

    return response.json()

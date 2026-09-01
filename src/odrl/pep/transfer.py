import requests


def delegate_to(endpoint: str, data: dict):
    """Delegate a task to an endpoint and wait for its result."""
    response = requests.post(endpoint, data=data)
    response.raise_for_status()

    return response.json()

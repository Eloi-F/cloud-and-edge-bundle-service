def transfer_to(endpoint: str, data: dict | None) -> bool:
    """Transfer data to an endpoint without expecting a response."""
    return True


def delegate_to(endpoint: str, data: dict):
    """Delegate a task to an endpoint and wait for its result."""
    pass

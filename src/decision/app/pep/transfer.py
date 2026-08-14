ENDPOINTS = {"aggregator": "http://localhost:8001/test"}


def transfer_to(target: str, data: dict) -> bool:
    print(ENDPOINTS[target])
    return True

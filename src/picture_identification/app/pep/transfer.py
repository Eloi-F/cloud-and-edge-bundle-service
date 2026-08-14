ENDPOINTS = {"dataset": "http://localhost:8001/dataset"}


def transfer_to(target: str, data: dict) -> bool:
    print(ENDPOINTS[target])
    return True

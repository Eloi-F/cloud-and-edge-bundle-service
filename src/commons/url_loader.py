import json
import os
from pathlib import Path

_CONFIG_PATH = Path(__file__).resolve().parent / "urls_config.json"
print(_CONFIG_PATH)

with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
    _CONFIG = json.load(f)

SERVICES = _CONFIG["capacities"]


def load_urls_config() -> dict:
    """Return the parsed JSON config as a dict."""
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_service_url(capacity: str) -> str:
    return SERVICES["urn:capacity:" + capacity]
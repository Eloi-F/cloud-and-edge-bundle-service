"""
Bundle Service Abstraction Layer
================================

This module replaces the previous FastAPI-based gateway.

It provides direct access to external services used by the PiCar system:

- decision service (speed / control)
- identification service (computer vision)
- trajectory planning service (route generation)

This module acts as a lightweight client wrapper.
"""
import requests
from config import BundleConfig

config = BundleConfig()


def decision(payload: dict) -> dict:
    """
    Send sensor data to the decision service.
    Returns updated control values (e.g. speed).
    """
    url = f"{config.edge_base_url}{config.endpoint_decision}"
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


def get_identification(payload: dict) -> dict:
    """
    Send image data to the identification service.
    Returns detected objects.
    """
    url = f"{config.cloud_base_url}{config.endpoint_identification}"
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


def get_trajectory_planning(payload: dict) -> bytes:
    """
    Request a route map from trajectory planning service.
    Returns raw HTML content.
    """
    url = f"{config.cloud_base_url}{config.endpoint_trajectory}"
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.content

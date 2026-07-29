"""
Bundle Service Abstraction Layer
================================

This module provides client wrappers for the external services used by the
PiCar-X application.

It exposes functions to communicate with:
- the decision service,
- the identification service,
- the trajectory planning service.
"""
import requests
from odrl_eval.policy_manager import bundle_config


def call_decision(payload: dict) -> dict:
    """
    Sends sensor data to the decision service.

    :param payload: Sensor data sent to the service.

    :return: The JSON response containing the updated control values.
    """
    response = requests.post(bundle_config["decision"].endpoint, json=payload)
    response.raise_for_status()
    return response.json()


def get_identification(payload: dict) -> dict:
    """
    Sends an image to the identification service.

    :param payload: Encoded image payload.

    :return: The JSON response containing the identification results.
    """
    response = requests.post(bundle_config["identification"].endpoint, json=payload)
    response.raise_for_status()
    return response.json()


def get_trajectory_planning(payload: dict) -> bytes:
    """
    Requests a route from the trajectory planning service.

    :param payload: Route request containing the start and destination addresses.

    :return: The generated HTML map as raw bytes.
    """
    response = requests.post(bundle_config["navigation"].endpoint, json=payload)
    response.raise_for_status()
    return response.content

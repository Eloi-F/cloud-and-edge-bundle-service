import threading
import requests
from app.core.config import ORCHESTRATOR_DOMAIN
from app.discovery.policy_manager import PolicyManager


def send_now():
    data = PolicyManager.get_odrl()
    try:
        response = requests.post(f"http://{ORCHESTRATOR_DOMAIN}/discovery", json=data)
        response.raise_for_status()
        print("Capabilities sent successfully.")
    except requests.RequestException as e:
        print(f"Error communicating with the Orchestrator: {e}")


def send_periodically(stop_event: threading.Event, waiting_time: int = 30):
    while not stop_event.is_set():
        send_now()
        stop_event.wait(waiting_time)

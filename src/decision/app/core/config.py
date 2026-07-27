import os
import socket

POLICIES_PATH = os.getenv("POLICIES_PATH", "./policies")
ORCHESTRATOR_DOMAIN = os.getenv("ORCHESTRATOR_DOMAIN", "example_orchestrator.com")


PORT = int(os.getenv("PORT", 8002))
HOST_DOMAIN = os.getenv("HOST_DOMAIN", "127.0.0.1")

PROTOCOL = os.getenv("PROTOCOL", "http")
BASE_URL = f"{PROTOCOL}://{HOST_DOMAIN}:{PORT}"

NODE_ID = os.getenv("NODE_ID", socket.gethostname())

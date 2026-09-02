import os
import socket


PORT = int(os.getenv("PORT", 8003))
HOST_DOMAIN = os.getenv("HOST_DOMAIN", "127.0.0.1")

PROTOCOL = os.getenv("PROTOCOL", "http")
BASE_URL = f"{PROTOCOL}://{HOST_DOMAIN}:{PORT}"

NODE_ID = os.getenv("NODE_ID", socket.gethostname())

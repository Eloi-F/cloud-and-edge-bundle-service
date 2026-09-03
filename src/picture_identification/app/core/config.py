import os
import socket


PORT = int(os.getenv("PORT", 8000))
HOST_DOMAIN = os.getenv("HOST_DOMAIN", "127.0.0.1")

PROTOCOL = os.getenv("PROTOCOL", "http")
BASE_URL = f"{PROTOCOL}://{HOST_DOMAIN}:{PORT}"

NODE_ID = os.getenv("NODE_ID", socket.gethostname())

MODEL_PATH = os.getenv(
    "YOLO_MODEL_PATH", "./src/picture_identification/models/yolo26x.pt"
)

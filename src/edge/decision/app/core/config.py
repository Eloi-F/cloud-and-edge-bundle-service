import os

POLICIES_PATH = os.getenv("POLICIES_PATH", "./policies")
ORCHESTRATOR_DOMAIN = os.getenv("ORCHESTRATOR_DOMAIN", "example_orchestrator.com")
PORT = int(os.getenv("PORT", 8002))

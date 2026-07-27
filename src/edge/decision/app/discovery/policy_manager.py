import json
import os
import threading
from app.core.config import POLICIES_PATH


class PolicyManager:
    _odrl_graph: dict = {}
    _lock = threading.Lock()

    @staticmethod
    def _read_files() -> dict:
        graph = []
        if not os.path.exists(POLICIES_PATH):
            return {"@context": "http://www.w3.org/ns/odrl.jsonld", "@graph": graph}

        for filename in os.listdir(POLICIES_PATH):
            if not filename.endswith(".json") or filename == "template-policy.json":
                continue

            filepath = os.path.join(POLICIES_PATH, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                graph.append(json.load(f))

        return {
            "@context": "http://www.w3.org/ns/odrl.jsonld",
            "@graph": graph,
        }

    @classmethod
    def reload_odrl(cls):
        new_graph = cls._read_files()
        with cls._lock:
            cls._odrl_graph = new_graph
        print("ODRL policies reloaded")

    @classmethod
    def get_odrl(cls) -> dict:
        with cls._lock:
            return cls._odrl_graph.copy()

from dataclasses import dataclass
import os
import json


@dataclass(frozen=True)
class BundleConfig:
    cloud_base_url: str = "http://[cloud-server-ip]:8000"
    edge_base_url: str = "http://[edge-server-ip]:8000"

    endpoint_decision: str = "/decision"
    endpoint_identification: str = "/identification"
    endpoint_trajectory: str = "/trajectory_planning"


class OdrlEvaluator:
    def __init__(self, policies_path="./policies"):
        self.policies_path = policies_path

    def import_odrl(self):
        graph = []

        for filename in os.listdir(self.policies_path):
            if not filename.endswith(".json") or filename == "template-policy.json":
                continue

            filepath = os.path.join(self.policies_path, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                policy = json.load(f)

            graph.append(policy)

        return {"@context": "http://www.w3.org/ns/odrl.jsonld", "@graph": graph}


class Service:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port

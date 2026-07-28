from dataclasses import dataclass
import json
from pathlib import Path

from core.config import ORCHESTRATOR_DOMAIN, POLICIES_PATH

import requests


@dataclass
class Service:
    ip: str
    port: int
    endpoint: str

    @property
    def url(self):
        return f"http://{self.ip}:{self.port}{self.endpoint}"


class BundleConfig:
    def __init__(self):
        self.port: int = 8000
        self.cloud_ip: str = "[cloud-server-ip]"
        self.edge_ip: str = "[edge-server-ip]"
        self.policies_path = Path(POLICIES_PATH)

        self.endpoints = {
            "decision": "/decision",
            "identification": "/identification",
            "navigation": "/navigation",
        }

        self.bundle_decision: dict[str, Service] = {}

        self.validated_odrl = self.initialisation()
        self.odrl_to_config(self.validated_odrl)

    def initialisation(self) -> dict:
        graph = []
        for policy_file in self.policies_path.glob("*.json"):
            if policy_file.name == "template-policy.json":
                continue

            policy = json.loads(policy_file.read_text(encoding="utf-8"))
            if self.ask_orchestrator(policy):
                graph.append(policy)

        return {
            "@context": "http://www.w3.org/ns/odrl.jsonld",
            "@graph": graph,
        }

    def ask_orchestrator(self, policy) -> bool:
        reply = requests.post(ORCHESTRATOR_DOMAIN, json=policy)

        try:
            reply.raise_for_status()
        except requests.HTTPError as e:
            raise RuntimeError(
                f"There was an error when contacting the Orchestrator: {e}"
            ) from e

        result = reply.json()
        success = result.get("result")
        if success is True:
            return True
        elif success is False:
            reason = result.get("reason")
            constraints = [
                f"{c['leftOperand']} {c['operator']} {c['rightOperand']}"
                for c in reason
            ]

            print(
                "There is no service available that is compliant with these constraints: "
                + ", ".join(constraints)
            )

            return False
        else:
            raise RuntimeError(f"Unexpected API response: {result}")

    def odrl_to_config(self, odrl: dict):
        for policy in odrl["@graph"]:
            service_name = policy["uid"].split(":")[-1]

            target = policy["duty"]["target"].split(":")[-1]

            if target == "edge":
                ip = self.edge_ip
            elif target == "cloud":
                ip = self.cloud_ip
            else:
                raise ValueError(f"Unknown target: {target}")

            endpoint = self.endpoints[service_name]

            self.bundle_decision[service_name] = Service(
                ip=ip,
                port=self.port,
                endpoint=endpoint,
            )


bundle_config = BundleConfig()

from dataclasses import dataclass, field
import json
import os


@dataclass
class Service:
    ip: str
    port: int
    endpoint: str

    @property
    def url(self):
        return f"http://{self.ip}:{self.port}{self.endpoint}"


@dataclass
class BundleConfig:
    port: int = 8000
    cloud_ip: str = "[cloud-server-ip]"
    edge_ip: str = "[edge-server-ip]"
    policies_path: str = "./policies"

    endpoints: dict = field(
        default_factory=lambda: {
            "decision": "/decision",
            "identification": "/identification",
            "navigation": "/navigation",
        }
    )

    bundle: dict[str, Service] = field(default_factory=dict)

    def import_odrl(self) -> dict:
        graph = []

        for filename in os.listdir(self.policies_path):
            if not filename.endswith(".json") or filename == "template-policy.json":
                continue

            filepath = os.path.join(self.policies_path, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                graph.append(json.load(f))

        return {
            "@context": "http://www.w3.org/ns/odrl.jsonld",
            "@graph": graph,
        }

    @classmethod
    def from_odrl(cls):
        config = cls()
        odrl = config.import_odrl()
        config.odrl_to_config(odrl)
        return config

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

            self.bundle[service_name] = Service(
                ip=ip,
                port=self.port,
                endpoint=endpoint,
            )


bundle_config = BundleConfig.from_odrl().bundle

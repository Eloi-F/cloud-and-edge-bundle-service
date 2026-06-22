from dataclasses import dataclass


@dataclass(frozen=True)
class BundleConfig:
    cloud_base_url: str = "http://[cloud-server-ip]:8000"
    edge_base_url: str = "http://[edge-server-ip]:8000"

    endpoint_decision: str = "/decision"
    endpoint_identification: str = "/identification"
    endpoint_trajectory: str = "/trajectory_planning"

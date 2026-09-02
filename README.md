# Cloud and Edge Bundle Service

## Overview

This repository contains a distributed architecture for managing bundle processing across local, edge, and cloud
environments.

The system is composed of:

* a local client application running on the vehicle;
* edge/cloud capacities that process the data, each enforcing its behavior through ODRL policies.

Each capacity is a FastAPI microservice that can be deployed independently.

## Bundles

The pipeline is driven by **bundle policies** expressed in ODRL. Each request carries a `bundle_id` that selects
the policy to enforce. Capacities validate permissions (`verify_permissions`) and execute obligations
(`enforce_duties`), delegating to the next capacity through a `nextPolicy` duty.

| Bundle   | Pipeline                                                                 |
| -------- | ------------------------------------------------------------------------ |
| bundle1  | `image_compression` → `identification` → `data_storage`                  |
| bundle2  | `image_compression` → `identification` → `decision` → `data_storage`     |
| bundle3  | `navigation` (trajectory planning)                                       |

## Project Structure

* **`src/<capacity>/`**: One directory per capacity (`data_storage`, `decision`, `image_compression`, `navigation`,
  plus `picture_identification` for the identification capacity).
* **`src/commons/`**: Shared Pydantic request/response schemas.
* **`src/odrl/`**: Shared ODRL policy engine (`odrl_eval`) and policy-enforcement point (`pep`).
* **`src/logging_config/`**: Shared logging configuration helper.
* **`src/local/`**: Vehicle client application.
* **`docker/`**: Dockerfiles used to build the different service images.

## Capacities and ports

| Capacity            | Port | Endpoint                |
| ------------------- | ---- | ----------------------- |
| picture_identification | 8000 | `/identification`     |
| navigation          | 8001 | `/trajectory_planning`  |
| decision            | 8002 | `/decision`             |
| image_compression   | 8003 | `/resize`               |
| data_storage        | 8004 | `/storage`              |

## Installation

### Build Docker Images

1. Clone the repository:

```sh
git clone https://github.com/Eloi-F/cloud-and-edge-bundle-service.git
```

2. Build the required containers from the repository root:

```sh
docker build -f docker/decision.Dockerfile -t decision .
docker build -f docker/identification.Dockerfile -t identification .
docker build -f docker/navigation.Dockerfile -t navigation .
docker build -f docker/image_compression.Dockerfile -t image_compression .
docker build -f docker/data_storage.Dockerfile -t data_storage .
docker build -f docker/local.Dockerfile -t local .
```

## Configuration

Each service has its own configuration requirements.

For more information about installation, configuration, and usage, refer to the `README.md` file located in the
corresponding service directory.

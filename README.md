# Cloud and Edge Bundle Service

## Overview

This repository contains a distributed architecture for managing bundle processing across local, edge, and cloud
environments.

The system is composed of:

* a local client application running on the vehicle;
* edge/cloud capacities that process the data and call each other through plain HTTP.

Each capacity is a FastAPI microservice that can be deployed independently.

## Bundles

A request carries a `bundle_id` that selects which pipeline to run. Capacities call each other directly over HTTP
(no policy engine involved).

| Bundle   | Pipeline                                                                 |
| -------- | ------------------------------------------------------------------------ |
| bundle1  | `image_compression` → `identification` → `data_storage`                  |
| bundle2  | `image_compression` → `identification` → `decision` → `data_storage`     |
| bundle3  | `navigation` (trajectory planning)                                       |

## Project Structure

* **`src/<capacity>/`**: One directory per capacity (`data_storage`, `decision`, `image_compression`, `navigation`,
  plus `picture_identification` for the identification capacity).
* **`src/models/`**: Shared Pydantic request/response schemas.
* **`src/http_client.py`**: Shared helper for plain HTTP calls between capacities.
* **`src/client.py`**: Test client that runs the three bundles against the running services.
* **`src/logging_config/`**: Shared logging configuration helper.
* **`src/local/`**: Vehicle client application (kept separate, still uses its own ODRL evaluation).
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

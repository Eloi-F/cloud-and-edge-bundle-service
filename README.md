# Cloud and Edge Bundle Service

## Overview

This repository contains a distributed architecture for managing bundle processing across local, edge, and cloud environments.

The system is composed of:

* a local client application running on the vehicle;
* edge services responsible for processing close to the data source;
* multiple cloud services providing higher-level processing and capabilities.

Each component can be deployed independently using Docker.

## Project Structure

* **`src/local/`**: Contains the vehicle client application responsible for local processing and communication with edge and cloud services.
* **`src/edge/`**: Contains the edge platform components and services.
* **`src/cloud/`**: Contains the different cloud services and their related components.
* **`docker/`**: Contains the Dockerfiles used to build the different service images.

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
docker build -f docker/local.Dockerfile -t local .
```

## Configuration

Each service has its own configuration requirements.

For more information about installation, configuration, and usage, refer to the `README.md` file located in the corresponding service directory.

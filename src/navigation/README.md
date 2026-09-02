# Navigation capacity

## Role

The `navigation` capacity is responsible for **trajectory / shortest-path planning** between two addresses.
It corresponds to **bundle 3** of the bundle-processing pipeline.

It is a FastAPI microservice exposing a single `/trajectory_planning` endpoint.

## How it works

1. A client sends a `TrajectoryRequest` (start/destination addresses, ODRL metadata, bundle id) to `POST /trajectory_planning`.
2. `verify_permissions(evaluator, bundle_id, metadata)` checks the request against the ODRL policy of the bundle
   (see `src/navigation/policies/navigation.jsonld`). Access is denied with `401` otherwise.
3. The response is currently a placeholder `{"success": "True"}`.

> Note: the actual path computation is implemented in `src/navigation/app/core/trajectory_logic.py`
> (`build_trajectory_map`), which calls the Google Maps Directions API and renders a Folium map, but its usage
> in `main.py` is currently commented out. Because `trajectory_logic.py` raises an `EnvironmentError` when
> `GOOGLE_MAPS_API_KEY` is not set, it must not be imported unless the key is configured.

## Behavior per bundle

| Bundle | Policy file        | Behavior                                                 |
| ------ | ------------------ | -------------------------------------------------------- |
| bundle3| `navigation.jsonld`| Validate the request (path computation currently disabled). |

## Running

From the repository root, with the virtual environment active:

```sh
python3 -m src.navigation.main
```

The service listens on port `8001` (overridable with the `PORT` environment variable).

## Requirements

Install the dependencies declared in `src/navigation/requirements.txt`:

```sh
pip install -r src/navigation/requirements.txt
```

## Environment Variables

| Variable              | Description                                      | Default                         |
| --------------------- | ------------------------------------------------ | ------------------------------- |
| `GOOGLE_MAPS_API_KEY` | API key used to access the Google Maps services. | `n/a`                           |
| `POLICIES_PATH`       | Path to the directory containing ODRL policies.  | `./policies`                    |
| `ORCHESTRATOR_DOMAIN` | The domain anycast used by orchestrators.        | `example_orchestrator.com`      |
| `PORT`                | Port on which the application listens.           | `8001`                          |
| `HOST_DOMAIN`         | Host domain or IP address of the service.        | `127.0.0.1`                     |
| `PROTOCOL`            | Protocol used to build the service base URL.     | `http`                          |
| `NODE_ID`             | Unique identifier of the service node.           | `System hostname`               |

> Note: `main.py` hard-codes the policies directory
> (`ODRLEvaluator("./src/navigation/policies")`) instead of reading `POLICIES_PATH`.

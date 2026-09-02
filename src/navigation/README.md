# Navigation capacity

## Role

The `navigation` capacity is responsible for **trajectory / shortest-path planning** between two addresses.
It corresponds to **bundle 3** of the bundle-processing pipeline.

It is a FastAPI microservice exposing a single `/trajectory_planning` endpoint.

## How it works

1. A client sends a `TrajectoryRequest` (start/destination addresses, bundle id) to `POST /trajectory_planning`.
2. The response is currently a placeholder `{"success": "True"}`.

> Note: the actual path computation is implemented in `src/navigation/app/core/trajectory_logic.py`
> (`build_trajectory_map`), which calls the Google Maps Directions API and renders a Folium map, but its usage
> in `main.py` is currently commented out. Because `trajectory_logic.py` raises an `EnvironmentError` when
> `GOOGLE_MAPS_API_KEY` is not set, it must not be imported unless the key is configured.

## Behavior per bundle

| Bundle | Behavior                                                 |
| ------ | -------------------------------------------------------- |
| bundle3| Validate the request (path computation currently disabled). |

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
| `PORT`                | Port on which the application listens.           | `8001`                          |
| `GOOGLE_MAPS_API_KEY` | API key used to access the Google Maps services. | `n/a`                           |

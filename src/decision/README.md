# Decision capacity

## Role

The `decision` capacity computes a **driving speed instruction** from the detections produced by the
identification capacity and the current vehicle sensor readings. It is used in **bundle 2** of the
bundle-processing pipeline.

It is a FastAPI microservice exposing a single `/decision` endpoint.

## How it works

1. A client sends a `DecisionRequest` (image, detections, sensors, ODRL metadata, bundle id) to `POST /decision`.
2. `verify_permissions(evaluator, bundle_id, metadata)` checks the request against the ODRL policy of the bundle
   (see `src/decision/policies/decision.jsonld`). Access is denied with `401` if the action is not allowed.
3. If the permission is granted, the speed is computed by `calculate_speed(dist, cliff_state)` in
   `src/decision/app/core/speed_logic.py`.
4. The pending ODRL duties are then executed by `enforce_duties(...)`. In bundle 2 the policy declares a
   `nextPolicy` duty towards `urn:capacity:storage`, so the resulting `TrainingData` (image, detections, speed)
   is delegated to the storage capacity (`http://localhost:8004/storage`).
5. The computed speed is returned as a `DecisionResponse`.

## Behavior per bundle

| Bundle | Policy file            | Behavior                                                        |
| ------ | ---------------------- | --------------------------------------------------------------- |
| bundle2| `decision.jsonld`      | Compute speed, then delegate the training data to `storage`.    |

Bundle 1 and bundle 3 do not pass through this capacity in the current pipeline.

## Speed logic

`calculate_speed(dist, cliff_state)` in `src/decision/app/core/speed_logic.py`:

* returns `0` when the obstacle is too close (`dist <= 10`) or a cliff is detected;
* returns `100` when the path is clear (`dist >= 90`);
* otherwise interpolates linearly: `1.25 * dist - 12.5`.

## Running

From the repository root, with the virtual environment active:

```sh
python3 -m src.decision.main
```

The service listens on port `8002` (overridable with the `PORT` environment variable).

## Requirements

Install the dependencies declared in `src/decision/requirements.txt`:

```sh
pip install -r src/decision/requirements.txt
```

## Environment Variables

| Variable              | Description                                      | Default                         |
| --------------------- | ------------------------------------------------ | ------------------------------- |
| `POLICIES_PATH`       | Path to the directory containing ODRL policies.  | `./policies`                    |
| `ORCHESTRATOR_DOMAIN` | The domain anycast used by orchestrators.        | `example_orchestrator.com`      |
| `PORT`                | Port on which the application listens.           | `8002`                          |
| `HOST_DOMAIN`         | Host domain or IP address of the service.        | `127.0.0.1`                     |
| `PROTOCOL`            | Protocol used to build the service base URL.     | `http`                          |
| `NODE_ID`             | Unique identifier of the service node.           | `System hostname`               |

> Note: the `main.py` currently hard-codes the policies directory
> (`ODRLEvaluator("./src/decision/policies")`) instead of reading `POLICIES_PATH` from `config.py`.

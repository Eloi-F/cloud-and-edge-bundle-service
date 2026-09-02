# Decision capacity

## Role

The `decision` capacity computes a **driving speed instruction** from the detections produced by the
identification capacity and the current vehicle sensor readings. It is used in **bundle 2** of the
bundle-processing pipeline.

It is a FastAPI microservice exposing a single `/decision` endpoint.

## How it works

1. A client sends a `DecisionRequest` (image, detections, sensors, bundle id) to `POST /decision`.
2. The speed is computed by `calculate_speed(dist, cliff_state)` in
   `src/decision/app/core/speed_logic.py`.
3. The resulting `TrainingData` (image, detections, speed) is forwarded to the storage capacity
   (`http://localhost:8004/storage`) through a plain HTTP call.
4. The computed speed is returned as a `DecisionResponse`.

## Behavior per bundle

| Bundle | Behavior                                                        |
| ------ | --------------------------------------------------------------- |
| bundle2| Compute speed, then store the training data in `data_storage`.  |

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
| `PORT`                | Port on which the application listens.           | `8002`                          |
| `STORAGE_URL`         | URL of the `data_storage` `/storage` endpoint.   | `http://localhost:8004/storage` |

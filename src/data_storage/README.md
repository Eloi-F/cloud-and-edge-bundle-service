# Data Storage capacity

## Role

The `data_storage` capacity **persists training samples** (image, detections, speed) into a local SQLite
database (`training.db`). Stored samples are meant to be reused later for training AI models. It is the
terminal step of **bundles 1 and 2**.

It is a FastAPI microservice exposing a single `/storage` endpoint.

## How it works

1. On startup, `create_storage()` in `src/data_storage/app/core/storage_logic.py` creates the SQLite schema
   if it does not exist (three tables: `bounding_boxes`, `detections`, `training`).
2. A client (usually the decision or identification capacity) sends a `TrainingData` request to `POST /storage`.
3. `verify_permissions(evaluator, bundle_id, metadata)` checks the request against the ODRL policy of the bundle
   (see `src/data_storage/policies/bundle1.jsonld` and `bundle2.jsonld`). Access is denied with `401` otherwise.
4. `store_sample(image, speed, detections)` inserts:
   * the image and speed into the `training` table;
   * one row per detection into `bounding_boxes` (box coordinates) and `detections` (class, confidence, box, training id).
5. Any pending ODRL duties are executed by `enforce_duties(...)` (the current policies declare none).
6. A boolean result is returned (True if the sample was stored, False on error).

## Behavior per bundle

| Bundle | Policy file  | Behavior                                                        |
| ------ | ------------ | --------------------------------------------------------------- |
| bundle1| `bundle1.jsonld` | Store an image + detections sample (speed is `None`).       |
| bundle2| `bundle2.jsonld` | Store an image + detections + speed sample.                 |

## Database schema

```sql
training        (id, img, speed)
bounding_boxes  (id, x, y, width, height)
detections      (id, classID, conf, boxID, trainingID)   -- FK boxID -> bounding_boxes, trainingID -> training
```

## Running

From the repository root, with the virtual environment active:

```sh
python3 -m src.data_storage.main
```

The service listens on port `8004` (overridable with the `PORT` environment variable). The database file
`training.db` is created in the current working directory.

## Requirements

Install the dependencies declared in `src/data_storage/requirements.txt`:

```sh
pip install -r src/data_storage/requirements.txt
```

## Environment Variables

| Variable              | Description                                      | Default                         |
| --------------------- | ------------------------------------------------ | ------------------------------- |
| `POLICIES_PATH`       | Path to the directory containing ODRL policies.  | `./policies`                    |
| `ORCHESTRATOR_DOMAIN` | The domain anycast used by orchestrators.        | `example_orchestrator.com`      |
| `PORT`                | Port on which the application listens.           | `8004`                          |
| `HOST_DOMAIN`         | Host domain or IP address of the service.        | `127.0.0.1`                     |
| `PROTOCOL`            | Protocol used to build the service base URL.     | `http`                          |
| `NODE_ID`             | Unique identifier of the service node.           | `System hostname`               |

> Note: `main.py` hard-codes the policies directory
> (`ODRLEvaluator("./src/data_storage/policies")`) instead of reading `POLICIES_PATH`.

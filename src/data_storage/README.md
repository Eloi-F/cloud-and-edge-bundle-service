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
3. `store_sample(image, speed, detections)` inserts:
   * the image and speed into the `training` table;
   * one row per detection into `bounding_boxes` (box coordinates) and `detections` (class, confidence, box, training id).
4. A boolean result is returned (True if the sample was stored, False on error).

## Behavior per bundle

| Bundle | Behavior                                                        |
| ------ | --------------------------------------------------------------- |
| bundle1| Store an image + detections sample (speed is `None`).       |
| bundle2| Store an image + detections + speed sample.                 |

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
| `PORT`                | Port on which the application listens.           | `8004`                          |

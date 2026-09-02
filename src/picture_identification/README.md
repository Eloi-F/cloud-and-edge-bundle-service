# Picture Identification capacity

## Role

The `picture_identification` capacity performs **AI object recognition** on an input image to detect obstacles
on the road, using a YOLO model. It sits in the middle of **bundles 1 and 2**.

It is a FastAPI microservice exposing a single `/identification` endpoint.

## How it works

1. A client sends an `IdentificationRequest` (base64 image, optional sensors, bundle id) to `POST /identification`.
2. `identify_objects(image)` in `src/picture_identification/app/core/identification_logic.py` decodes the image and
   runs the YOLO model to produce a list of `Detection` objects.
3. Depending on the bundle (see below) the result is forwarded to the next capacity through a plain HTTP call.

## Behavior per bundle

| Bundle | Behavior                                                                  |
| ------ | ------------------------------------------------------------------------- |
| bundle1| Forward the image + detections to `data_storage`, return the detections.  |
| bundle2| Forward the image + detections + sensors to `decision`, return the speed. |

## Running

From the repository root, with the virtual environment active:

```sh
python3 -m src.picture_identification.main
```

The service listens on port `8000` (overridable with the `PORT` environment variable). It loads the YOLO model
(configured via `YOLO_MODEL_PATH`, default `./models/yolo26x.pt`) at startup.

## Requirements

Install the dependencies declared in `src/picture_identification/requirements.txt`:

```sh
pip install -r src/picture_identification/requirements.txt
```

## Environment Variables

| Variable              | Description                                              | Default                                 |
| --------------------- | -------------------------------------------------------- | --------------------------------------- |
| `PORT`                | Port on which the application listens.                   | `8000`                                  |
| `YOLO_MODEL_PATH`     | Path to the YOLO model used by the application.          | `./models/yolo26x.pt`                   |
| `STORAGE_URL`         | URL of the `data_storage` `/storage` endpoint.           | `http://localhost:8004/storage`         |
| `DECISION_URL`        | URL of the `decision` `/decision` endpoint.              | `http://localhost:8002/decision`        |

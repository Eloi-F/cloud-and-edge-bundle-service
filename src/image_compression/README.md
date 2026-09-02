# Image Compression capacity

## Role

The `image_compression` capacity **resizes an input image** to a fixed `640x640` format (with letterbox
padding) before it is sent to the identification capacity. It acts as a preprocessing front-end for
**bundles 1 and 2**.

It is a FastAPI microservice exposing a single `/resize` endpoint.

## How it works

1. A client sends an `IdentificationRequest` (base64 image, optional sensors, bundle id) to `POST /resize`.
2. The image is resized by `crop_with_padding(image)` in `src/image_compression/app/core/crop.py`:
   * decode the base64 image;
   * scale it to fit within `640x640` (LANCZOS resampling);
   * paste it centered on a grey (`114,114,114`) canvas;
   * re-encode to JPEG and return as base64.
3. A new `IdentificationRequest` is built with the resized image and forwarded to the identification capacity
   (`http://localhost:8000/identification`) through a plain HTTP call.
4. The result returned to the caller depends on the bundle (see below).

## Behavior per bundle

| Bundle | Behavior                                                                 |
| ------ | ------------------------------------------------------------------------ |
| bundle1| Resize image, forward to identification, return the `detections`.   |
| bundle2| Resize image, forward to identification, return the `speed` instruction. |

## Running

From the repository root, with the virtual environment active:

```sh
python3 -m src.image_compression.main
```

The service listens on port `8003` (overridable with the `PORT` environment variable).

## Requirements

Install the dependencies declared in `src/image_compression/requirements.txt`:

```sh
pip install -r src/image_compression/requirements.txt
```

## Environment Variables

| Variable              | Description                                              | Default                                 |
| --------------------- | -------------------------------------------------------- | --------------------------------------- |
| `PORT`                | Port on which the application listens.                   | `8003`                                  |
| `IDENTIFICATION_URL`  | URL of the `identification` `/identification` endpoint.  | `http://localhost:8000/identification`  |

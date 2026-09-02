# Image Compression capacity

## Role

The `image_compression` capacity **resizes an input image** to a fixed `640x640` format (with letterbox
padding) before it is sent to the identification capacity. It acts as a preprocessing front-end for
**bundles 1 and 2**.

It is a FastAPI microservice exposing a single `/resize` endpoint.

## How it works

1. A client sends an `IdentificationRequest` (base64 image, optional sensors, ODRL metadata, bundle id) to `POST /resize`.
2. `verify_permissions(evaluator, bundle_id, metadata)` checks the request against the ODRL policy of the bundle
   (see `src/image_compression/policies/bundle1.jsonld` and `bundle2.jsonld`). Access is denied with `401` otherwise.
3. The image is resized by `crop_with_padding(image)` in `src/image_compression/app/core/crop.py`:
   * decode the base64 image;
   * scale it to fit within `640x640` (LANCZOS resampling);
   * paste it centered on a grey (`114,114,114`) canvas;
   * re-encode to JPEG and return as base64.
4. A new `IdentificationRequest` is built with the resized image, then `enforce_duties(...)` executes the pending
   ODRL duties. Both bundle policies declare a `nextPolicy` duty towards `urn:capacity:identification`, so the
   resized image is delegated to the identification capacity (`http://localhost:8000/identification`).
5. The result returned to the caller depends on the bundle (see below).

## Behavior per bundle

| Bundle | Policy file  | Behavior                                                                 |
| ------ | ------------ | ------------------------------------------------------------------------ |
| bundle1| `bundle1.jsonld` | Resize image, delegate to identification, return the `detections`.   |
| bundle2| `bundle2.jsonld` | Resize image, delegate to identification, return the `speed` instruction. |

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

| Variable              | Description                                      | Default                         |
| --------------------- | ------------------------------------------------ | ------------------------------- |
| `POLICIES_PATH`       | Path to the directory containing ODRL policies.  | `./policies`                    |
| `ORCHESTRATOR_DOMAIN` | The domain anycast used by orchestrators.        | `example_orchestrator.com`      |
| `PORT`                | Port on which the application listens.           | `8003`                          |
| `HOST_DOMAIN`         | Host domain or IP address of the service.        | `127.0.0.1`                     |
| `PROTOCOL`            | Protocol used to build the service base URL.     | `http`                          |
| `NODE_ID`             | Unique identifier of the service node.           | `System hostname`               |

> Notes:
> * `main.py` hard-codes the policies directory
>   (`ODRLEvaluator("./src/image_compression/policies")`) instead of reading `POLICIES_PATH`.
> * `src/image_compression/app/core/config.py` declares a default `PORT` of `8002`, which conflicts with the
>   decision capacity. This file is not imported by `main.py`, which uses `PORT` (default `8003`).

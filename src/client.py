import argparse
import base64
import random
import sys
import time
from datetime import datetime


import requests

ODRL = "http://www.w3.org/ns/odrl/2/"

DEFAULT_IMAGE = "image.png"

ENDPOINTS = {
    "resize": "http://localhost:8003/resize",
    "trajectory": "http://localhost:8001/trajectory_planning",
}

BUNDLES = ("bundle1", "bundle2", "bundle3")

BUNDLE_IDS = {
    "bundle1": "urn:policy:bundle:bundle1",
    "bundle2": "urn:policy:bundle:bundle2",
    "bundle3": "urn:policy:bundle:bundle3",
}

# ODRL permission context used by the image_compression service policies.
COMPRESSION_PARTY = "urn:capacity:compression"
COMPRESSION_ACTION = "urn:action:compute-compression"

# ODRL permission context used by the navigation service policy.
NAVIGATION_PARTY = "urn:capacity:navigation"
NAVIGATION_ACTION = "urn:action:compute-path"

ASSET_INPUT = "urn:data:input"


def make_metadata(party: str, action: str, when: str | None = None) -> dict:
    """Build ODRL metadata with a dynamic (current) dateTime by default."""
    return {
        ODRL + "dateTime": when or datetime.now().isoformat(),
        ODRL + "Party": party,
        ODRL + "Action": action,
        ODRL + "Asset": ASSET_INPUT,
    }


def load_image(path: str) -> str:
    """Return a base64-encoded JPEG. Falls back to a tiny placeholder if missing."""
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"[warn] Image not found at '{path}', using a placeholder image.")
        sys.exit()


def build_bundle1(image: str) -> dict:
    return {
        "bundle_id": BUNDLE_IDS["bundle1"],
        "metadata": make_metadata(COMPRESSION_PARTY, COMPRESSION_ACTION),
        "image": image,
        "sensors": None,
    }


def build_bundle2(
    image: str,
    front: float | None = None,
    state: bool | None = None,
) -> dict:
    return {
        "bundle_id": BUNDLE_IDS["bundle2"],
        "metadata": make_metadata(COMPRESSION_PARTY, COMPRESSION_ACTION),
        "image": image,
        "sensors": {
            "front": front
            if front is not None
            else round(random.uniform(5.0, 200.0), 2),
            "state": state if state is not None else random.choice([True, False]),
        },
    }


def build_bundle3(start_address: str, destination_address: str) -> dict:
    return {
        "bundle_id": BUNDLE_IDS["bundle3"],
        "metadata": make_metadata(NAVIGATION_PARTY, NAVIGATION_ACTION),
        "start_address": start_address,
        "destination_address": destination_address,
    }


def run_bundle(bundle: str, args: argparse.Namespace) -> tuple[float, dict]:
    """Build the payload, POST it, and return (elapsed_seconds, response_json)."""
    if bundle == "bundle1":
        url, payload = args.resize_url, build_bundle1(args.image)
    elif bundle == "bundle2":
        url, payload = args.resize_url, build_bundle2(
            args.image, args.front, args.state
        )
    else:
        url, payload = args.trajectory_url, build_bundle3(args.start, args.destination)

    print(f"[{bundle}] POST {url}", flush=True)

    start = time.perf_counter()
    response = requests.post(url, json=payload, timeout=args.timeout)
    elapsed = time.perf_counter() - start

    response.raise_for_status()
    return elapsed, response.json()


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bundle test client. Launches one or several bundle tests "
        "against the running services and reports timings."
    )
    parser.add_argument(
        "--bundle",
        choices=BUNDLES,
        action="append",
        help="Bundle(s) to run (repeatable). Defaults to all if --all is not set.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run every bundle.",
    )

    parser.add_argument(
        "--image", default=DEFAULT_IMAGE, help="Path to the input image."
    )
    parser.add_argument("--start", default="Tripode A", help="Start address (bundle3).")
    parser.add_argument(
        "--destination",
        default="7 avenue colonel roche",
        help="Destination address (bundle3).",
    )
    parser.add_argument(
        "--front",
        type=float,
        default=None,
        help="Front distance in meters (bundle2). Random if omitted.",
    )
    parser.add_argument(
        "--state",
        type=lambda v: v.lower() in ("true", "1", "yes"),
        default=None,
        help="Cliff state, true/false (bundle2). Random if omitted.",
    )
    parser.add_argument(
        "--resize-url", default=ENDPOINTS["resize"], help="image_compression endpoint."
    )
    parser.add_argument(
        "--trajectory-url",
        default=ENDPOINTS["trajectory"],
        help="navigation endpoint.",
    )
    parser.add_argument(
        "--timeout", type=float, default=60.0, help="HTTP timeout in seconds."
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)

    to_run = list(dict.fromkeys(args.bundle)) if args.bundle else []
    if args.all or not to_run:
        to_run = list(BUNDLES)

    results = {}
    for bundle in to_run:
        try:
            elapsed, body = run_bundle(bundle, args)
            results[bundle] = elapsed
            print(f"[{bundle}] response: {body}")
            print(f"[{bundle}] elapsed:  {elapsed * 1000:.1f} ms")
        except requests.RequestException as exc:
            print(f"[{bundle}] ERROR: {exc}", file=sys.stderr)
            results[bundle] = None
        print()

    print("---- timing summary ----")
    for bundle in to_run:
        elapsed = results.get(bundle)
        label = f"{elapsed * 1000:.1f} ms" if elapsed is not None else "FAILED"
        print(f"{bundle:8s} {label}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

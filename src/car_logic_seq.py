"""
Autonomous PiCar-X Client
=========================

This script controls a PiCar-X robot and coordinates three main tasks:

1. Line following (circulation):
   - Uses the grayscale sensors to follow a line.
   - Adjusts steering and motor speed according to the detected line position.

2. Obstacle detection (detection):
   - Reads the ultrasonic sensor.
   - Sends distance information to a remote service.
   - Receives an updated speed value from the server.

3. Object/person identification:
   - Sends a picture to the identification server
   - Receives the picture annotated with the objects detected and a box around them

Additionally, the script requests a route from a remote service, downloads an HTML map, and opens it in a browser.
"""

import threading

from src.common.latency_measurments.metrics import SeqMetrics

from src.common.services.identification import identification
from src.common.services.detection import detection
from src.common.services.navigation import trajectory_planning
from src.common.local.line_following import circulation


def run_sequential_logic(cycle: int, scenario: str = "bundle"):
    line_following_t = threading.Thread(
        target=circulation,
        name="circulation",
    )
    try:
        trajectory_planning("Tripode A", "7 avenue colonel roche")
        line_following_t.start()
        for _ in range(cycle):
            detection()
            identification()
            SeqMetrics.update_round_latencies()

    except KeyboardInterrupt:
        print("Ctrl+C pressed. Stopping...")
        line_following_t.join()

    finally:
        SeqMetrics.save_response_times_to_file(
            scenario, SeqMetrics.get_latencies(), "./data/sequential_lat.json"
        )


if __name__ == "__main__":
    scenario = "full_cloud"
    run_sequential_logic(10, scenario)

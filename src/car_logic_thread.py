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
   - Runs in a dedicated thread through the imported `identification` module.

Additionally, the script requests a route from a remote service, downloads an HTML map, and opens it in a browser.

Architecture
------------
The application relies on multiple threads:

- circulation()        : robot navigation and line following
- detection()          : obstacle detection and speed control
- identification()     : image/object recognition (external module)
"""
import threading

from src.common.latency_measurments.metrics import ConcurrentMetrics

from src.common.services.identification import identification
from src.common.services.detection import detection
from src.common.services.navigation import trajectory_planning
from src.common.local.line_following import circulation


def run_threaded_logic(cycle_by_service: dict[str, int], scenario: str = "bundle"):
    """
    Application entry point.

    Workflow
    --------
    1. Retrieve bundle configuration from the server.
    2. Request route planning information.
    3. Start navigation, detection, and identification threads.
    4. Wait indefinitely for all threads.
    """
    thread_circ = threading.Thread(
        target=circulation,
        name="circulation",
    )

    thread_det = threading.Thread(
        target=detection,
        args=(cycle_by_service.get("detection"),),
        name="detection",
    )

    thread_id = threading.Thread(
        target=identification,
        args=(cycle_by_service.get("identification"),),
        name="identification",
    )

    try:
        trajectory_planning("Tripode A", "7 avenue colonel roche")

        thread_circ.start()
        thread_det.start()
        thread_id.start()

        thread_circ.join()
        thread_det.join()
        thread_id.join()

    except KeyboardInterrupt:
        print("Ctrl+C pressed. Stopping...")
        thread_circ.join()
        thread_det.join()
        thread_id.join()

    finally:
        ConcurrentMetrics.save_response_times_to_file(
            scenario, ConcurrentMetrics.get_latencies(), "./data/parallel_lat.json"
        )


if __name__ == "__main__":
    scenario = "full_cloud"
    cycle_by_service = {"detection": 50, "identification": 20}
    run_threaded_logic(cycle_by_service, scenario)

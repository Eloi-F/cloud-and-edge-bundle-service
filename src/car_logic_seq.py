"""
Autonomous PiCar-X Client
=========================

This module coordinates the sequential execution of the PiCar-X application.

The circulation task runs in its own thread, while the detection and
identification services are executed sequentially for a fixed number of cycles.

Before starting the execution, a route is requested from the navigation service.
When the benchmark completes, collected latency measurements are saved.
"""

import threading

from src.common.latency_measurments.metrics import SeqMetrics

from src.common.services.identification import identification
from src.common.services.detection import detection
from src.common.services.navigation import trajectory_planning
from src.common.local.line_following import circulation


def run_sequential_logic(cycle: int, scenario: str = "bundle"):
    """
    Runs the sequential version of the application.

    Workflow:
    1. Request a route from the navigation service.
    2. Start the circulation thread.
    3. Execute detection and identification sequentially for the specified
       number of cycles.
    4. Update latency metrics after each cycle.
    5. Save latency measurements before exiting.

    :param cycle: Number of sequential execution cycles.
    :param scenario: Benchmark scenario used when saving latency metrics.
    """
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
    scenario = "bundle"
    run_sequential_logic(10, scenario)

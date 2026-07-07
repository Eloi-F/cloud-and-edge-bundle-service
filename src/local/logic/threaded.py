"""
Autonomous PiCar-X Client
=========================

This module coordinates the multithreaded execution of the PiCar-X application.

Three independent threads are started:

- circulation: Handles line following and robot navigation.
- detection: Performs obstacle detection.
- identification: Runs image/object identification.

Before starting the threads, a route is requested from the navigation service.
When the application terminates, collected latency measurements are saved.
"""
import threading

from latency_measurements.metrics import ConcurrentMetrics

from services.identification import identification
from services.detection import detection
from services.navigation import trajectory_planning
from core.line_following import circulation


def run_threaded_logic(cycle_by_service: dict[str, int], scenario: str):
    """
    Runs the multithreaded version of the application.

    Workflow:
    1. Request a route from the navigation service.
    2. Create the circulation, detection, and identification threads.
    3. Start all threads.
    4. Wait for all threads to complete.
    5. Save latency measurements before exiting.

    :param cycle_by_service: Execution cycle for each service.
    :param scenario: Benchmark scenario used when saving latency metrics.
    """
    stop_event = threading.Event()
    thread_circ = threading.Thread(
        target=circulation,
        args=(stop_event,),
        name="circulation",
    )

    thread_det = threading.Thread(
        target=detection,
        args=(stop_event, cycle_by_service.get("detection"), True),
        name="detection",
    )

    thread_id = threading.Thread(
        target=identification,
        args=(stop_event, cycle_by_service.get("identification"), True),
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
        stop_event.set()
        thread_circ.join()
        thread_det.join()
        thread_id.join()

    finally:
        ConcurrentMetrics.save_response_times_to_file(
            scenario, ConcurrentMetrics.get_latencies(), "./data/parallel_lat.json"
        )

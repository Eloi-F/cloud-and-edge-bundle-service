import threading

from services.identification import identification
from services.detection import detection
from services.navigation import trajectory_planning
from core.line_following import circulation


def run_threaded_logic():
    """
    Runs the multithreaded version of the application.

    Workflow:
    1. Request a route from the navigation service.
    2. Create the circulation, detection, and identification threads.
    3. Start all threads.
    4. Wait for all threads to complete.
    5. Save latency measurements before exiting.
    """
    stop_event = threading.Event()
    thread_circ = threading.Thread(
        target=circulation,
        args=(stop_event,),
        name="circulation",
    )

    thread_det = threading.Thread(
        target=detection,
        args=(stop_event,),
        name="detection",
    )

    thread_id = threading.Thread(
        target=identification,
        args=(stop_event,),
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


def main():
    run_threaded_logic()


if __name__ == "__main__":
    main()

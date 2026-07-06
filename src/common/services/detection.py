import threading

from picarx import Picarx

from src.common.local.bundle import decision_parallel, decision_seq

px = Picarx()
px_power: int = 10

lock = threading.Lock()


def detection(
    stop_event: threading.Event,
    cycle: int = 100,
    parallel_exec: bool = False,
):
    """
    Performs obstacle detection and updates the robot speed.

    The ultrasonic and grayscale sensors are read, and their data is sent to
    either the sequential or parallel decision service. The returned speed is
    stored in the shared `px_power` variable.

    In sequential mode, the function processes a single iteration and returns.
    In parallel mode, it repeats the process for the specified number of cycles.

    :param cycle: Number of iterations in parallel mode.
    :param parallel_exec: Selects the parallel or sequential endpoint.
    """
    global px_power

    for _ in range(cycle):
        if stop_event.is_set():
            break
        ultrasonic_percept = px.ultrasonic.read()
        gm_val_list = px.get_grayscale_data()
        gm_state = px.get_cliff_status(gm_val_list)
        data = {"front": ultrasonic_percept, "state": gm_state}

        # Measure network latency
        if parallel_exec:
            response = decision_parallel(payload=data)
        else:
            response = decision_seq(payload=data)

        with lock:
            px_power = response.get("speed", 0)

        if not parallel_exec:
            return

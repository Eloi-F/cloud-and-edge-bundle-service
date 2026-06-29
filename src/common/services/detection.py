import threading

from picarx import Picarx

from src.common.local.bundle import decision_parallel, decision_seq

px = Picarx()
px_power: int = 10

lock = threading.Lock()


def detection(cycle: int = 100, parallel_exec: bool = False):
    """
    Obstacle detection and adaptive speed control.

    Responsibilities
    ----------------
    - Read the ultrasonic sensor.
    - Send distance information to a remote service.
    - Measure request latency.
    - Receive and apply a new speed value.
    """
    global px_power

    for _ in range(cycle):
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

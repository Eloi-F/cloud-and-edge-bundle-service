import threading

from picarx import Picarx

from core.bundle import call_decision

px = Picarx()
px_power: int = 10

lock = threading.Lock()


def detection(stop_event: threading.Event):
    """
    Performs obstacle detection and updates the robot speed.

    The ultrasonic and grayscale sensors are read, and their data is sent to
    either the sequential or parallel decision service. The returned speed is
    stored in the shared `px_power` variable.
    """
    global px_power

    while not stop_event.is_set():
        ultrasonic_percept = px.ultrasonic.read()
        gm_val_list = px.get_grayscale_data()
        gm_state = px.get_cliff_status(gm_val_list)
        data = {"front": ultrasonic_percept, "state": gm_state}

        response = call_decision(payload=data)

        with lock:
            px_power = response.get("speed", 0)

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
from time import sleep

from picarx import Picarx

from src.common.latency_measurments.metrics import SeqMetrics

from src.common.services.identification import identification
from src.common.services.detection import detection
from src.common.services.navigation import trajectory_planning

from src.common.services.detection import px_power

px = Picarx()
current_state: str | None = None
offset: int = 20

# Last valid line-following state
# Used when the line is temporarily lost
last_state: str = "stop"
lock = threading.Lock()


def _outHandle():
    """
    Recovery procedure executed when the line is lost.
    """
    global last_state, current_state

    if last_state == "left":
        px.set_dir_servo_angle(-30)
        px.backward(10)

    elif last_state == "right":
        px.set_dir_servo_angle(30)
        px.backward(10)

    while True:
        gm_val_list = px.get_grayscale_data()
        gm_state = _get_status(gm_val_list)

        currentSta = gm_state

        # Exit recovery mode once the sensor state changes
        if currentSta != last_state:
            break

    sleep(0.001)


def _get_status(val_list: list[int]):
    """
    Convert grayscale sensor readings into a navigation command.
    """
    _state = px.get_line_status(val_list)

    # Left sensor sees the line
    if _state[0] == 1:
        return "right"

    # Center sensor sees the line
    elif _state[1] == 1:
        return "forward"

    # Right sensor sees the line
    elif _state[2] == 1:
        return "left"

    # No line detected
    else:
        return "stop"


def circulation():
    """
    Main line-following control loop.

    Responsibilities
    ----------------
    - Read grayscale sensors.
    - Determine line position.
    - Adjust steering angle.
    - Drive the robot forward.
    - Trigger recovery mode when the line is lost.

    Runs continuously until the program exits.
    """
    global last_state
    try:
        while True:
            # Read line sensors
            gm_val_list = px.get_grayscale_data()
            gm_state = _get_status(gm_val_list)

            # Keep track of the most recent valid direction
            if gm_state != "stop":
                last_state = gm_state

            # Steering logic
            if gm_state == "forward":
                px.set_dir_servo_angle(0)
                px.forward(px_power)

            elif gm_state == "left":
                px.set_dir_servo_angle(offset)
                px.forward(px_power)

            elif gm_state == "right":
                px.set_dir_servo_angle(-offset)
                px.forward(px_power)

            else:
                # Attempt to recover the line
                _outHandle()

    finally:
        px.stop()


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
        SeqMetrics.save_response_times_to_file(
            scenario, SeqMetrics.get_latencies(), "./data/sequential_lat.json"
        )


if __name__ == "__main__":
    scenario = "full_cloud"
    run_sequential_logic(10, scenario)

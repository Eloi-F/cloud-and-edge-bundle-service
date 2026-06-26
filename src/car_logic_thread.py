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
import webbrowser
from time import sleep

from picarx import Picarx

from src.common.local.identification import identification
from src.common.local.bundle import decision, get_trajectory_planning

px = Picarx()
current_state: str | None = None
px_power: int = 10
offset: int = 20

# Last valid line-following state
# Used when the line is temporarily lost
last_state: str = "stop"
lock = threading.Lock()


def outHandle():
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
        gm_state = get_status(gm_val_list)

        currentSta = gm_state

        # Exit recovery mode once the sensor state changes
        if currentSta != last_state:
            break

    sleep(0.001)


def get_status(val_list: list[int]):
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
            gm_state = get_status(gm_val_list)

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
                outHandle()

    finally:
        px.stop()


def detection():
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

    while True:
        ultrasonic_percept = px.ultrasonic.read()
        gm_val_list = px.get_grayscale_data()
        gm_state = px.get_cliff_status(gm_val_list)
        data = {"front": ultrasonic_percept, "state": gm_state}

        # Measure network latency
        response = decision(payload=data)

        with lock:
            px_power = response.get("speed", 0)


def trajectory_planning(start_address: str, destination_address: str):
    """
    Request a route from the remote planning service.

    Responsibilities
    --------
    - Sends a start and destination address.
    - Receives an HTML map.
    - Saves the map locally.
    - Opens it in the default browser.
    """
    data = {
        "start_address": start_address,
        "destination_address": destination_address,
    }

    response = get_trajectory_planning(payload=data)

    with open("received_map.html", "wb") as f:
        f.write(response)

    print("Map saved as received_map.html")
    webbrowser.open("received_map.html")


def run_threaded_logic():
    """
    Application entry point.

    Workflow
    --------
    1. Retrieve bundle configuration from the server.
    2. Request route planning information.
    3. Start navigation, detection, and identification threads.
    4. Wait indefinitely for all threads.
    """
    # Measure route planning latency
    trajectory_planning("Tripode A", "7 avenue colonel roche")

    thread1 = threading.Thread(
        target=circulation,
        name="circulation",
    )

    thread2 = threading.Thread(
        target=detection,
        name="detection",
    )

    thread3 = threading.Thread(
        target=identification,
        name="identification",
    )

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()


if __name__ == "__main__":
    run_threaded_logic()

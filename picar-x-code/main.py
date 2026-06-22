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

from picarx import Picarx
from time import sleep
import time
import threading
import requests
from identification import identification
import webbrowser
import json

px = Picarx()
current_state = None
px_power = 10
offset = 20

# Last valid line-following state
# Used when the line is temporarily lost
last_state = "stop"
lock = threading.Lock()

# Stores latency measurements
responses = []
responses_cloud = []


def save_response_times_to_file(filename="cloud_edge_response_latency.json"):
    """
    Save recorded latency measurements to a JSON file.
    """
    with open(filename, "w") as f:
        json.dump(responses, f)

    print(f"Temps de réponse sauvegardés dans {filename}")


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


def get_status(val_list):
    """
    Convert grayscale sensor readings into a navigation command.
    """
    _state = px.get_line_status(val_list)

    if _state == [0, 0, 0]:
        return "stop"

    # Left sensor sees the line
    elif _state[0] == 1:
        return "right"

    # Center sensor sees the line
    elif _state[1] == 1:
        return "forward"

    # Right sensor sees the line
    elif _state[2] == 1:
        return "left"


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


def detection(api, endpoint):
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
    response_data = []

    while True:
        ultrasonic_percept = px.ultrasonic.read()

        data = {
            "front": ultrasonic_percept,
            "vitesse": px_power,
        }

        # Measure network latency
        t1 = time.time()
        url = f"http://[bundle-server-ip]:8000/{api}/{endpoint}"
        response = requests.post(url=url, json=data)
        t2 = time.time()

        response_data.append((t2 - t1) * 1000)

        print("latency detection [edge] = ", (t2 - t1) * 1000)

        with lock:
            px_power = response.json()["vitesse"]


def trajectory_planning(api, endpoint):
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
        "start_address": "Tripode A",
        "end_address": "7 avenue colonel roche",
    }

    url = f"http://[bundle-server-ip]:8000/{api}/{endpoint}"

    response = requests.post(url=url, json=data)

    if response.status_code == 200:
        with open("received_map.html", "wb") as f:
            f.write(response.content)

        print("Map saved as received_map.html")
        webbrowser.open("received_map.html")

    else:
        print(f"Failed to retrieve map: " f"{response.status_code} - {response.text}")


if __name__ == "__main__":
    """
    Application entry point.

    Workflow
    --------
    1. Retrieve bundle configuration from the server.
    2. Request route planning information.
    3. Start navigation, detection, and identification threads.
    4. Wait indefinitely for all threads.
    """

    reponse = requests.get(url="http://[bundle-server-ip]:8000/get-bundle")

    data = reponse.json()

    # Measure route planning latency
    t1 = time.time()
    trajectory_planning(data["api"], data["endpoint3"])
    t2 = time.time()

    print("delay trajectory [cloud] = ", (t2 - t1) * 1000)

    # Navigation thread
    thread1 = threading.Thread(target=circulation)

    # Obstacle detection thread
    thread2 = threading.Thread(
        target=detection,
        args=(
            data["api"],
            data["endpoint1"],
        ),
    )

    # Identification thread
    thread3 = threading.Thread(
        target=identification,
        args=(
            responses_cloud,
            data["api"],
            data["endpoint2"],
        ),
    )

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

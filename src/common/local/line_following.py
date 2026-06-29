from time import sleep
from picarx import Picarx

from src.common.services.detection import px_power

OFFSET: int = 20
px = Picarx()


def _outHandle(last_state: str):
    """
    Attempts to recover the line when it is no longer detected.

    The robot reverses while steering toward the last known direction until
    the grayscale sensors detect a different line state.

    :param last_state: Last detected line position.
    """
    if last_state == "left":
        px.set_dir_servo_angle(-30)
        px.backward(10)

    elif last_state == "right":
        px.set_dir_servo_angle(30)
        px.backward(10)

    while True:
        gm_val_list = px.get_grayscale_data()
        gm_state = _get_status(gm_val_list)

        # Exit recovery mode once the sensor state changes
        if gm_state != last_state:
            break

        sleep(0.001)


def _get_status(val_list: list[int]):
    """
    Converts grayscale sensor readings into a navigation command.

    :param val_list: Raw grayscale sensor values.

    :return str: One of "forward", "left", "right", or "stop".
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
    Continuously performs line following.

    The grayscale sensors are used to determine the line position, adjust the
    steering angle, and drive the robot using the current shared speed value.
    If the line is lost, a recovery procedure is executed.

    The function runs until the application terminates.
    """

    # Last valid line-following state
    # Used when the line is temporarily lost
    last_state: str = ""

    try:
        while True:
            # Read line sensors
            gm_val_list = px.get_grayscale_data()
            last_state = _get_status(gm_val_list)

            # Steering logic
            if last_state == "forward":
                px.set_dir_servo_angle(0)
                px.forward(px_power)

            elif last_state == "left":
                px.set_dir_servo_angle(OFFSET)
                px.forward(px_power)

            elif last_state == "right":
                px.set_dir_servo_angle(-OFFSET)
                px.forward(px_power)

            else:
                # Attempt to recover the line
                _outHandle(last_state)

    finally:
        px.stop()

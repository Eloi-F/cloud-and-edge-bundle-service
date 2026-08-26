def calculate_speed(dist: float, cliff_state: bool, detections):
    """
    Returns speed percentage to adopt, based on linear
    formula.

    :param dist: Distance to the obstacle
    :param cliff_state: True if a cliff is detected ahead, otherwise False
    :param detections: The detections mades by the identification endpoint
    :return float: Speed percentage to apply
    """
    if cliff_state or dist <= 10:
        return 0
    elif dist >= 90:
        return 100
    else:
        # f : dist ∈ [10;90] |---> [0;100]
        return 1.25 * dist - 12.5

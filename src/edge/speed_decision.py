def speed_decision(dist, cliff_state):
    """
    Returns speed percentage to adopt, based on linear
    formula.
    :param dist: distance to object
    :param cliff_state: boolean telling if there's a cliff ahead
    :return int: speed percentage to adopt
    """
    if cliff_state or dist <= 10:
        return 0
    elif dist >= 90:
        return 100
    else:
        # f : dist ∈ [10;90] |---> [0;100]
        return 1.25 * dist - 12.5

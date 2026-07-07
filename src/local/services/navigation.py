import webbrowser

from core.bundle import get_trajectory_planning


def trajectory_planning(start_address: str, destination_address: str):
    """
    Requests a route from the trajectory planning service.

    The generated HTML map is saved locally as `received_map.html`
    and opened in the default web browser.

    :param start_address: Starting location of the route.
    :param destination_address: Destination of the route.
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

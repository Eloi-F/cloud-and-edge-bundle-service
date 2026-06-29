import webbrowser

from src.common.local.bundle import get_trajectory_planning


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

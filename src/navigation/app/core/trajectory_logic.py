import logging

from fastapi import HTTPException
from osmnx import geocoder, distance, routing, graph

logger = logging.getLogger(__name__)


def _street_name(edge) -> str | None:
    name = edge.get("name")
    if name is None:
        return None
    if isinstance(name, list):
        return " / ".join(name)
    return name


def compute_shortest_path(
        city_map: graph.MultiDiGraph,
        start_address: str,
        destination_address: str
) -> list[str] :
    """
    Performs shortest path determination for given
    addresses.
    :param city_map:
    :param start_address:
    :param destination_address:
    :return: list of streets to cross
    """

    try :
        osm_start_coords = geocoder.geocode(start_address)
        osm_dest_coords = geocoder.geocode(destination_address)
        logger.debug("Determined coordinates of start address (%s) and destination address (%s)",
                     osm_start_coords, osm_dest_coords)

        osm_start_id = distance.nearest_nodes(
            city_map,
            osm_start_coords[1],
            osm_start_coords[0],
        )
        osm_dest_id = distance.nearest_nodes(
            city_map,
            osm_dest_coords[1],
            osm_dest_coords[0],
        )
        logger.debug("Determined id of start address (%s) and destination address (%s)",
                     osm_start_id, osm_dest_id)

        route = routing.shortest_path(
            city_map,
            osm_start_id,
            osm_dest_id,
            weight="length"
        )

        streets = []
        for u, v in zip(route[:-1], route[1:]):
            edge = next(iter(city_map[u][v].values()))
            name = _street_name(edge)
            if name is not None and (not streets or streets[-1] != name):
                streets.append(name)
        logger.debug("Compute path : %s", streets)

        return streets
    except Exception:
        logger.error("Could not identify given address.")
        raise HTTPException(status_code=204,detail="Error on given addresses")

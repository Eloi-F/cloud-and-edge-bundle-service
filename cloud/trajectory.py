import googlemaps
from datetime import datetime
import folium
import polyline

api_key = "AIzaSyDHwXSGLEdQVpmU6qJPk4xVpfWzOycTfVI"
gmaps = googlemaps.Client(key=api_key)


def trajectory(start_address, destination_address):
    directions_result = gmaps.directions(
        start_address,
        destination_address,
        mode="driving",
        departure_time=datetime.now(),
    )

    route = directions_result[0]["overview_polyline"]["points"]
    points = polyline.decode(route)

    latitudes = [point[0] for point in points]
    longitudes = [point[1] for point in points]

    map_center = [latitudes[0], longitudes[0]]
    folium_map = folium.Map(location=map_center, zoom_start=13)

    route_coordinates = list(zip(latitudes, longitudes))
    folium.PolyLine(route_coordinates, color="blue", weight=5, opacity=0.7).add_to(
        folium_map
    )

    folium.Marker(
        location=[latitudes[0], longitudes[0]],
        popup="Départ",
        icon=folium.Icon(color="green"),
    ).add_to(folium_map)
    folium.Marker(
        location=[latitudes[-1], longitudes[-1]],
        popup="Arrivée",
        icon=folium.Icon(color="red"),
    ).add_to(folium_map)
    return folium_map

from fastapi import FastAPI, Request
import uvicorn
from identification import identification
from trajectory import trajectory
from fastapi.responses import FileResponse

app = FastAPI()


# identification capacity
@app.post("/identification")
async def read_root(request: Request):
    """
    Function called on POST request to identification endpoint.
    Call identification service on received image.
    Send back array of detected objects to the client.
    """
    data = await request.json()
    response = identification(data)
    return response


# trajectory planning capacity
@app.post("/trajectory_planning")
async def read_root(request: Request):
    """
    Function called on POST request to trajectory_planning endpoint.
    Call trajectory service on given start and destination addresses.
    Send back itinerary to the client.
    """
    data = await request.json()
    start_address = data["start_address"]
    destination_address = data["destination_address"]
    folium_map = trajectory(start_address, destination_address)
    map_file = "map.html"
    folium_map.save(map_file)
    return FileResponse(map_file, media_type="file", filename=map_file)


if __name__ == "__main__":
    # API's cloud Webserver
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)

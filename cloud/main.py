from fastapi import FastAPI, Request
import uvicorn
from identification import identification
from trajectory import trajectory
from fastapi.responses import FileResponse

app = FastAPI()


# identification capacitie
@app.post("/identification")
async def read_root(request: Request):
    data = await request.json()
    response = identification(data)
    return response


# trajectory planning capacitie
@app.post("/trajectory_planning")
async def read_root(request: Request):
    data = await request.json()
    start_address = data["start_address"]
    destination_address = data["destination_address"]
    folium_map = trajectory(start_address, destination_address)
    map_file = "map.html"
    folium_map.save(map_file)
    return FileResponse(map_file, media_type="file", filename=map_file)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)

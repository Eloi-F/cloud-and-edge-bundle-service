from fastapi import FastAPI, Request
import uvicorn
from speed_decision import speed_decision

app = FastAPI()

@app.post("/decision")
def read_root(data: dict):
    """
    Function called on POST request to decision endpoint.
    Send back speed instruction based on distance to
    object and current speed using speed_decision().

    :param data:
    :return: instruction
    """
    instruction={"speed":""}
    dist = data["front"]
    cliff_state = data["state"]
    instruction["speed"] = speed_decision(dist,cliff_state)
    return instruction

if __name__ == "__main__":
    # API's webserver
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
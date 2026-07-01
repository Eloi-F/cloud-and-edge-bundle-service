from fastapi import FastAPI
import uvicorn
from speed_decision import speed_decision

app = FastAPI()


@app.post("/decision")
def read_root(data: dict):
    """
    POST endpoint returning speed instruction based on:
    - distance to obstacle ("front")
    - cliff detection state ("state")

    Expected input format:
        {
            "front": float,
            "state": bool
        }

    Returns:
        {
            "speed": float
        }
    """
    dist = data["front"]
    cliff_state = data["state"]
    speed = speed_decision(dist, cliff_state)
    return {"speed": speed}


if __name__ == "__main__":
    # API's webserver
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)

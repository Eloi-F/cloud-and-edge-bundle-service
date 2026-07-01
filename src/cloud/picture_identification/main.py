from fastapi import FastAPI, Request
import uvicorn
from identification import identification

app = FastAPI()


# identification capacity
@app.post("/identification")
async def identification_endpoint(request: Request):
    """
    Function called on POST request to identification endpoint.
    Call identification service on received image.
    Send back array of detected objects to the client.
    """
    data = await request.json()
    response = identification(data)
    return response


if __name__ == "__main__":
    # API's cloud Webserver
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

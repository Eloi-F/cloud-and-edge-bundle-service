import uvicorn
import os

from fastapi import FastAPI

from app.api.schemas import IdentificationRequest, IdentificationResponse
from app.core.identification_logic import identify_objects
from odrl.pep.enforcer import enforce_odrl_policy

app = FastAPI()


@app.post("/identification", response_model=IdentificationResponse)
def identification(data: IdentificationRequest):
    enforce_odrl_policy(data.metadata)

    detections = identify_objects(data.image)
    return IdentificationResponse(detections=detections)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
    )

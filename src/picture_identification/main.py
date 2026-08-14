import uvicorn
from fastapi import FastAPI, HTTPException

from app.core.config import PORT
from app.api.schemas import IdentificationRequest, IdentificationResponse
from app.core.identification_logic import identify_objects

from odrl.odrl_eval import ODRLEvaluator

app = FastAPI()

# Initialize evaluator at startup (loading the unique graph)
evaluator = ODRLEvaluator("./policies")


@app.post("/identification", response_model=IdentificationResponse)
def identification(data: IdentificationRequest):
    if not evaluator.evaluate_and_enforce(data.metadata):
        raise HTTPException(
            status_code=401,
            detail="Forbidden by the data usage policy (ODRL).",
        )

    detections = identify_objects(data.image)

    return IdentificationResponse(detections=detections)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)

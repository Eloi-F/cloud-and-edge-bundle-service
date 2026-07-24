import uvicorn
from fastapi import FastAPI
from constraints_evaluator import (
    build_limitations,
    evaluate_request,
    build_requested_constraints
)

app = FastAPI(title="Orchestrator API", version="1.0.0")
LIMITATIONS = build_limitations()

@app.get("/")
def root():
    return {"message": "ODRL Evaluator API"}


@app.post("/demand")
def validate_constraints(policy: dict):
    print(evaluate_request(build_requested_constraints(policy),LIMITATIONS))

if __name__ == "__main__":
    # Start uvicorn endpoint
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Orchestrator API", version="1.0.0")


@app.get("/")
def root():
    return {"message": "ODRL Evaluator API"}


@app.post("/demand")
def validate_constraints(policy: dict):
    print(policy)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

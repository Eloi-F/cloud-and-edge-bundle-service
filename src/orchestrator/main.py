import json
import uvicorn
from fastapi import FastAPI

from constraints_evaluator import evaluate_request
from builder import build_limitations, build_requested_constraints
from models import OdrlPolicy, OdrlConstraint

app = FastAPI(title="Orchestrator API", version="1.0.0")
LIMITATIONS = build_limitations()

@app.get("/")
def root():
	return {"message": "ODRL Evaluator API"}

def serialize_response(result: tuple[bool, list[OdrlConstraint]]):
	return json.dumps({
		"result":result[0],
		"reason":result[1]
	})

@app.post("/demand")
def validate_constraints(policy: dict):
	"""
    POST orchestrator-side endpoint.
    Expect ODRL policy input format, asking for service resources allocations.
    Return ODRL policy format, clarifying access to remote host service.

    :param policy:
    :return: response
    """
	validated_policy = OdrlPolicy.model_validate(policy)
	request = build_requested_constraints(validated_policy)
	result = evaluate_request(request,LIMITATIONS)
	return serialize_response(result)


if __name__ == "__main__":
	# Start uvicorn endpoint
	uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

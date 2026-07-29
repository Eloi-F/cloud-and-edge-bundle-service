import json
import uvicorn
from fastapi import FastAPI

from constraints_evaluator import evaluate_request
from builder import build_limitations, build_requested_constraints
from models import OdrlSet, OdrlConstraint, OdrlGraph

app = FastAPI(title="Orchestrator API", version="1.0.0")
LIMITATIONS = build_limitations()


def serialize_response(result: tuple[bool, list[OdrlConstraint]]):
	return json.dumps({"result": result[0], "reason": result[1]})


@app.get("/")
def root():
	return {"message": "ODRL Evaluator API"}


@app.post("/server")
def handler_offer(offer:OdrlGraph):
	return


@app.post("/demand")
def validate_constraints(policy: OdrlSet):
	"""
	POST orchestrator-side endpoint.
	Expect ODRL policy input format, asking for service resources allocations.
	Return ODRL policy format, clarifying access to remote host service.

	:param policy:
	:return: response
	"""
	request = build_requested_constraints(policy)
	result = evaluate_request(request, LIMITATIONS)
	return serialize_response(result)



if __name__ == "__main__":
	# Start uvicorn endpoint
	# uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

	doody = OdrlGraph.model_validate({
    "@context": "http://www.w3.org/ns/odrl.jsonld",
    "@graph":
    [
        {
            "@context": "http://www.w3.org/ns/odrl.jsonld",
            "@type": "Offer",
            "uid": "urn:offer:service:decision",
            "assigner": "urn:node:dell-5799",
            "permission":
            [
                {
                    "target": "http://127.0.0.1:8002/decision",
                    "assignee": "urn:client:any",
                    "action": "use"
                }
            ],
            "obligation":
            [
                {
                    "target": "http://127.0.0.1:8002/decision",
                    "assignee": "urn:node:dell-5799",
                    "action": "urn:action:guarantee",
                    "constraint":
                    [
                        {
                            "leftOperand": "urn:metric:latency",
                            "operator": "lteq",
                            "rightOperand": 15,
                            "unit": "http://qudt.org/vocab/unit/MilliSEC"
                        },
                        {
                            "leftOperand": "urn:metric:encryption",
                            "operator": "eq",
                            "rightOperand": True
                        }
                    ]
                }
            ]
        },
        {
            "@context": "http://www.w3.org/ns/odrl.jsonld",
            "@type": "Offer",
            "uid": "urn:offer:service:navigation",
            "assigner": "urn:node:dell-5799",
            "permission":
            [
                {
                    "target": "http://127.0.0.1:8002/trajectory_planning",
                    "assignee": "urn:client:any",
                    "action": "use"
                }
            ],
            "obligation":
            [
                {
                    "target": "http://127.0.0.1:8002/trajectory_planning",
                    "assignee": "urn:node:dell-5799",
                    "action": "urn:action:guarantee",
                    "constraint":
                    [
                        {
                            "leftOperand": "urn:metric:encryption",
                            "operator": "eq",
                            "rightOperand": True
                        }
                    ]
                }
            ]
        },
        {
            "@context": "http://www.w3.org/ns/odrl.jsonld",
            "@type": "Offer",
            "uid": "urn:offer:service:testing",
            "assigner": "urn:node:dell-5799",
            "permission":
            [
                {
                    "target": "http://127.0.0.1:8002/testing",
                    "assignee": "urn:client:any",
                    "action": "use"
                }
            ],
            "obligation":
            [
                {
                    "target": "http://127.0.0.1:8002/testing",
                    "assignee": "urn:node:dell-5799",
                    "action": "urn:action:guarantee",
                    "constraint":
                    [
                        {
                            "leftOperand": "urn:metric:encryption",
                            "operator": "eq",
                            "rightOperand": True
                        }
                    ]
                }
            ]
        }
    ]
})


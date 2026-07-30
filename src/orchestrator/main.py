import json
import uvicorn
from fastapi import FastAPI
import asyncio

from src.orchestrator.server.builder import discover_topology, add_server, add_offer
from src.orchestrator.server.parser import parse_graph

from src.orchestrator.common.models import (
	OdrlConstraint
)
from src.orchestrator.server.models import (
	OfferingServerDict, OdrlGraph,
)

app = FastAPI(title="Orchestrator API", version="1.0.0")
OFFERS, OFFERS_LOCKER, SERVERS, SERVERS_LOCKER = discover_topology()


def serialize_response(result: tuple[bool, list[OdrlConstraint]]):
	return json.dumps({"result": result[0], "reason": result[1]})


@app.get("/")
def root():
	return {"message": "ODRL Evaluator API"}


@app.post("/server")
def handler_offer(offer:OdrlGraph):
	"""
	POST orchestrator-side endpoint exposed to servers.
	Expect ODRL policy input format, offering services host under constraints.
	Update OFFERS and SERVERS variables.
	TO BE DONE : Return Acknowledgment.

	:param offer:
	:return:
	"""
	server_id, server_url, server_offer = parse_graph(offer)
	add_server(SERVERS,SERVERS_LOCKER,server_id,server_url)
	add_offer(OFFERS,OFFERS_LOCKER,server_id,server_offer)
	return


@app.post("/demand")
def validate_constraints(policy: OdrlSet):
	"""
	POST orchestrator-side endpoint exposed to clients.
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
	uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

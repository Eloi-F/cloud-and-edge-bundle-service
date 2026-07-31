import json
import uvicorn
from fastapi import FastAPI

from server.builder import discover_topology, add_server, add_offer
from server.parser import parse_graph

from common.models import OdrlConstraint
from server.models import OdrlGraph
from car.models import OdrlRequest

from car.builder import build_request_payload
from car.constraints_evaluator import evaluate_request

import logging
from logging_config import setup_logging

logger = logging.getLogger(__name__)
setup_logging()

app = FastAPI(title="Orchestrator API", version="1.0.0")
OFFERS, OFFERS_LOCKER, SERVERS, SERVERS_LOCKER = discover_topology()


@app.get("/")
def root():
	logger.warning("T'es qui toi ?")
	return {"message": "Orchestrator API"}


@app.post("/server")
async def handler_offer(offer: OdrlGraph):
	"""
	POST orchestrator-side endpoint exposed to servers.
	Expect ODRL policy input format, offering services host under constraints.
	Update OFFERS and SERVERS variables.
	TO BE DONE : Return Acknowledgment.

	:param offer:
	:return:
	"""
	server_id, server_url, server_offer = parse_graph(offer)

	async with SERVERS_LOCKER:
		await add_server(SERVERS,server_id,server_url)

	async with OFFERS_LOCKER:
		await add_offer(OFFERS, server_id, server_offer)

	return


def serialize_response(result: tuple[bool, list[OdrlConstraint]]):
	return json.dumps({"result": result[0], "reason": result[1]})

@app.post("/demand")
def handle_requests(request: OdrlRequest):
	"""
	POST orchestrator-side endpoint exposed to clients.
	Expect ODRL policy input format, asking for service resources allocations.
	Return ODRL policy format, clarifying access to remote host service.

	:param request:
	:return: response
	"""
	payload_request = build_request_payload(request)
	result = evaluate_request(payload_request, OFFERS)
	return serialize_response(result)


if __name__ == "__main__":
	# Start application
	uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
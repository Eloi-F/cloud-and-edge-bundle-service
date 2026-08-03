import uvicorn
from fastapi import FastAPI

from common.registry import TopologyRegistry

from car.parser import parse_request
from car.models import OdrlRequest, OdrlAgreement

from server.parser import parse_offer
from server.models import OdrlGraph


import logging
from logging_config import setup_logging

logger = logging.getLogger(__name__)
setup_logging()

URN_ASSIGNEE = "urn:node"
URN_SEP = ":"

app = FastAPI(title="Orchestrator API", version="1.0.0")
topology = TopologyRegistry()



@app.get("/")
def root():
	logger.info("Received call on root.")
	return {"message": "Orchestrator API"}


@app.post("/server")
async def handle_offer(offer: OdrlGraph):
	"""
	POST orchestrator-side endpoint exposed to servers.
	Expect ODRL policy input format, offering services host under constraints.
	Update OFFERS and SERVERS variables.
	TO BE DONE : Return Acknowledgment.

	:param offer:
	:return:
	"""
	logger.info("Received new client request.")
	server_id, server_url, server_offer = parse_offer(offer)

	await topology.register_server(server_id,server_url)
	await topology.register_offer(server_id,server_offer)

	return


def serialize_response(request: OdrlRequest, server: str) -> OdrlAgreement:
	agreement = OdrlAgreement.model_validate(
		request.model_dump(by_alias=False) | {"type": "Agreement"}
	)
	agreement.obligation[0].assignee = URN_ASSIGNEE + URN_SEP + server
	return agreement

@app.post("/demand")
def handle_requests(request: OdrlRequest):
	"""
	POST orchestrator-side endpoint exposed to clients.
	Expect ODRL policy input format, asking for service resources allocations.
	Return ODRL policy format, clarifying access to remote host service.

	:param request:
	:return: response
	"""
	logger.info("Received new client request.")
	request_set = parse_request(request)
	capable_servers = topology.build_capable_servers(request_set)
	if capable_servers == {}:
		return {"code": 404}
	else:
		return serialize_response(request,topology.most_suitable_server(capable_servers))



if __name__ == "__main__":
	# Start application
	uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

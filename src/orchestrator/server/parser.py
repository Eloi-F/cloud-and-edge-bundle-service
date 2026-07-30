from models import (
	OdrlOffer,
	OdrlGraph,
	ServerOfferSet,
)
from src.orchestrator.common.models import (
	ConstraintValues
)

# URN format example :
# "urn:node:server"
URN_SEPARATOR = ":"

# URL format example :
# "http://server-ip:port/service"
URL_SEPARATOR = "/"

def add_offer(offers_set: ServerOfferSet, offer: OdrlOffer) -> ServerOfferSet:
	for obligation in offer.obligation :
		service =  obligation.target.rsplit(URL_SEPARATOR,1)[0]
		for constraint in obligation.constraints :
			metric = constraint.leftOperand.rsplit(URN_SEPARATOR,1)[-1]
			offers_set[service][metric] = ConstraintValues(
				constraint.operator,
				constraint.rightOperand
			)
	return offers_set

def get_server_info(offer: OdrlOffer) -> tuple[str,str]:
	server_id = offer.assigner.rsplit(":",1)[-1]
	server_url = offer.permission[0].target.rsplit(URL_SEPARATOR,1)[0]
	return server_id, server_url


def parse_offer_list(odrl_offers:list[OdrlOffer]) -> tuple[str,str,ServerOfferSet]:
	"""
	Parse a list of Odrl offers from a server and return
	server credentials and ConstraintSet of

	:param odrl_offers:
	:return: tuple(server_id,server_url,offers_set)
	"""
	server_id, server_url = get_server_info(odrl_offers[0])
	offers_set: ServerOfferSet = {}
	for offer in odrl_offers :
		add_offer(offers_set, offer)

	return server_id, server_url, offers_set


def parse_graph(graph: OdrlGraph) -> tuple[str,str,ServerOfferSet]:
	return parse_offer_list(graph.graph)

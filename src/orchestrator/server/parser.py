from server.models import (
	OdrlOffer,
	OdrlGraph
)
from common.models import (
	ConstraintValues,
	ServerOfferSet
)

from common.parser import parse_url, parse_urn

def add_offer(offers_set: ServerOfferSet, offer: OdrlOffer) -> ServerOfferSet:
	"""
	Add an offer (service and constraints) to a ServerOfferSet.

	:param offers_set:
	:param offer:
	:return: offers_set
	"""
	for obligation in offer.obligation :
		service =  parse_urn(obligation.target)
		for constraint in obligation.constraint :
			metric = parse_urn(constraint.leftOperand)
			if service not in offers_set :
				offers_set[service] = {}
			offers_set[service][metric] = ConstraintValues(
				constraint.operator,
				constraint.rightOperand
			)
	return offers_set

def get_server_info(offer: OdrlOffer) -> tuple[str,str]:
	"""
	Get server credentials (id and url) from an offer.

	:param offer:
	:return: id,url
	"""
	server_id = parse_urn(offer.assigner)
	server_url = parse_url(offer.permission[0].target)

	return server_id, server_url


def parse_offer_list(odrl_offers:list[OdrlOffer]) -> tuple[str,str,ServerOfferSet]:
	"""
	Parse a list of Odrl offers contained in a graph from a
	server and return server credentials and ServerOfferSet.

	:param odrl_offers:
	:return: tuple(server_id,server_url,offers_set)
	"""
	server_id, server_url = get_server_info(odrl_offers[0])
	offers_set: ServerOfferSet = {}
	for offer in odrl_offers :
		add_offer(offers_set, offer)

	return server_id, server_url, offers_set


def parse_graph(graph: OdrlGraph) -> tuple[str,str,ServerOfferSet]:
	"""Parse a received graph from a server"""
	return parse_offer_list(graph.graph)

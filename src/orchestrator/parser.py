from models import ConstraintValues, OdrlSet, OdrlGraph, OdrlOffer, ConstraintSet
from pathlib import Path


def parse_set_file(policy_file: Path) -> tuple[str, dict[str, ConstraintValues]]:
	policy = OdrlSet.model_validate_json(policy_file.read_text(encoding="utf-8"))
	return parse_set(policy)


def parse_set(policy: OdrlSet) -> tuple[str, dict[str, ConstraintValues]]:
	"""
	Parse a given policy file and return associated
	service and a dict of its constraints.

	:param policy:
	:return: tuple(service,constraint_dict)
	"""
	constraint_dict: dict[str, ConstraintValues] = {}

	service = policy.duty.assignee.rsplit(":", 1)[-1]

	for constraint in policy.duty.constraints:
		# Parse constraint name
		constraint_name = constraint.leftOperand.rsplit(":", 1)[-1]

		constraint_dict[constraint_name] = ConstraintValues(
			constraint.operator, constraint.rightOperand
		)

	return service, constraint_dict

def add_offer(offers_set: ConstraintSet, offer: OdrlOffer) -> ConstraintSet:
	for obligation in offer.obligation :
		service =  obligation.target.rsplit("/",1)[0]
		for constraint in obligation.constraints :
			metric = constraint.leftOperand.rsplit(":",1)[-1]
			offers_set[service][metric] = ConstraintValues(
				constraint.operator,
				constraint.rightOperand
			)
	return offers_set

def get_server_info(offer: OdrlOffer) -> tuple[str,str]:
	server_id = offer.assigner.rsplit(":",1)[-1]
	server_url = offer.permission[0].target.rsplit("/",1)[0]
	return server_id, server_url

def parse_offer_list(offers:list[OdrlOffer]) -> tuple[str,str,ConstraintSet]:
	"""
	Parse a received offer from a server and return its
	id, url to join it as well as all the services it
	can handle with the associated constraints.

	:param offers:
	:return: tuple(server_id,server_url,)
	"""
	server_id, server_url = get_server_info(offers[0])
	offers_set: ConstraintSet = {}
	for offer in offers :
		add_offer(offers_set, offer)

	return server_id, server_url, offers_set




def parse_graph(graph: OdrlGraph) -> tuple[str,str,ConstraintSet]:
	return parse_offer_list(graph.graph)


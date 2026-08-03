from car.models import OdrlRequest
from common.parser import parse_urn
from common.models import RequestSet, ConstraintValues
from pathlib import Path

import logging
logger = logging.getLogger(__name__)

def parse_set_file(policy_file: Path) -> RequestSet:
	"""Parse a request ODRL policy from a JSON file."""
	policy = OdrlRequest.model_validate_json(policy_file.read_text(encoding="utf-8"))
	return parse_request(policy)


def parse_request(request: OdrlRequest) -> RequestSet:
	"""
	Parse a given policy and return associated
	ConstraintSet.

	:param request:
	:return: tuple(service,constraint_dict)
	"""

	service = parse_urn(request.permission[0].target)
	request_set: RequestSet = {service: {}}

	for metric in request.obligation[0].constraint:
		# Parse constraint name
		metric_name = parse_urn(metric.leftOperand)

		request_set[service][metric_name] = ConstraintValues(
			metric.operator,
			metric.rightOperand
		)
		logger.info("Parsed new request from client.")

	return request_set

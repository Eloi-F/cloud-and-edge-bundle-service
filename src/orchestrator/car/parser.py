from car.models import ConstraintValues, OdrlRequest
from pathlib import Path


def parse_set_file(policy_file: Path) -> tuple[str, dict[str, ConstraintValues]]:
	policy = OdrlRequest.model_validate_json(policy_file.read_text(encoding="utf-8"))
	return parse_set(policy)


def parse_set(request: OdrlRequest) -> tuple[str, dict[str, ConstraintValues]]:
	"""
	Parse a given policy file and return associated
	service and a dict of its constraints.

	:param request:
	:return: tuple(service,constraint_dict)
	"""
	constraint_dict: dict[str, ConstraintValues] = {}

	service = request.permission[0].target.rsplit(":",1)[-1]

	for metric in request.obligation[0].constraint:
		# Parse constraint name
		metric_name = metric.leftOperand.rsplit(":", 1)[-1]

		constraint_dict[metric_name] = ConstraintValues(
			metric.operator, metric.rightOperand
		)

	return service, constraint_dict
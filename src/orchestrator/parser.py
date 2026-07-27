from models import Operand, ConstraintValues, OdrlPolicy
from pathlib import Path
import json


def parse_value(value: str) -> Operand:
	"""Parse the rightOperand value into its proper format"""
	if not isinstance(value,str):
		raise ValueError(f"Invalid value: {value} in ODRL file.")
	if value == "true":
		return True
	if value == "false":
		return False
	try:
		return int(value)
	except ValueError :
		pass
	try:
		return float(value)
	except ValueError :
		pass
	return value


def parse_policy_file(policy_file: Path) -> tuple[str, dict[str, ConstraintValues]] :
	return parse_policy(
		OdrlPolicy.model_validate(
			json.loads(policy_file.read_text(encoding="utf-8"))
		)
	)


def parse_policy(policy: OdrlPolicy) -> tuple[str, dict[str, ConstraintValues]] :
	"""
	Parse a given policy file and return associated
	service and a dict of its constraints.

	:param policy:
	:return: tuple(service,constraint_dict)
	"""
	constraint_dict : dict[str, ConstraintValues] = {}

	service = policy.duty.assignee.rsplit(":", 1)[-1]

	for constraint in policy.duty.constraint:
		# Parse constraint name
		constraint_name = constraint.leftOperand.rsplit(":", 1)[-1]

		constraint_dict[constraint_name] = ConstraintValues(
			constraint.operator,
			parse_value(constraint.rightOperand)
		)

	return service, constraint_dict
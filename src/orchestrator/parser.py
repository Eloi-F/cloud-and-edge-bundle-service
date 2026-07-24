from models import Constraint, Operator
from pathlib import Path
import json

def parse_value(value: str):
	"""Parse the rightOperand value into its proper format"""
	if value == "true":
		return True
	if value == "false":
		return False
	try:
		int_value = int(value)
		return int_value
	except ValueError :
		pass
	try:
		float_value = float(value)
		return float_value
	except ValueError :
		pass
	return value

def parse_policy(policy_file: Path) -> tuple[str,str,Constraint] :
	"""
	Parse a given orchestrator-side policy file and return
	relevant service, associated constraint and its values.

	:param policy_file:
	:return: tuple(service,constraint_name,constraint_values)
	"""
	policy = json.loads(policy_file.read_text(encoding="utf-8"))

	# Extract uid, operator and value from file
	try:
		uid = policy["uid"]
		operator = policy["duty"]["constraint"][0]["operator"]
		limit_value = policy["duty"]["constraint"][0]["rightOperand"]
	except KeyError as e:
		raise ValueError(f"Invalid ODRL file: {policy_file}") from e

	# Example UID format
	# urn:policy-id:services:navigation-check-latency
	policy_name = uid.rsplit(":",1)[-1]
	service, _, constraint_name = policy_name.partition("-check-")
	constraint_values = Constraint(Operator(operator),parse_value(limit_value))

	return service, constraint_name, constraint_values
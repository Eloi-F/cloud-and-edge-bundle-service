import json
from os import MFD_ALLOW_SEALING
from pathlib import Path
from dataclasses import dataclass
from xxlimited_35 import Null

from fastapi.utils import deep_dict_update

TEMPLATE_FILE = "templates-check"
POLICY_DIRECTORY = Path("./policies/")

@dataclass(frozen=True)
class Constraint:
	operator: str
	limit_value: str | int | float | bool

def parse_value(value: str):
	"""Parse the rightOperand value into its proper format"""
	if value == "true":
		return True
	if value == "false":
		return False
	try:
		int_value = int(value)
		return int_value
	except ValueError as e:
		pass
	try:
		float_value = float(value)
		return float_value
	except ValueError as e:
		pass
	return value


def parse_policy(policy_file: Path) -> tuple[str,str,Constraint] :
	"""
	Parse a given policy file and return associated relevant service,
	associated constraint and its values.

	:param policy_file:
	:return: tuple(service,constraint_name,constraint_values)
	"""
	# Open file
	policy = json.loads(policy_file.read_text(encoding="utf-8"))

	# Extract uid, operator and value from file
	try:
		uid = policy["uid"]
		operator = policy["duty"]["constraint"][0]["operator"]
		limit_value = policy["duty"]["constraint"][0]["rightOperand"]
	except KeyError as e:
		raise ValueError(f"Invalid ODRL file: {policy_file}") from e

	# Parse and return 
	# example uid format = urn:policy-id:services:navigation-check-latency
	policy_name = uid.rsplit(":",1)[-1]
	service, _, constraint_name = policy_name.partition("-check-")
	constraint_values = Constraint(operator,parse_value(limit_value))

	return service, constraint_name, constraint_values


def build_limitations() -> dict[str, dict[str, Constraint]]:
	"""
	Parse all ODRL policy files in /policies and build a
	dictionary of resource limitations indexed by service.

	:return: dict
        Structure of the form
        {
            "navigation": {
                "latency": Constraint(...),
                "frequency": Constraint(...)
            },
            ...
        }
	"""
	# Initialize returned dictionary and policies directory
	resources_limits = {}

	# For each orchestrator rule :
	for file in POLICY_DIRECTORY.iterdir():
		# Open and load every JSON files except templates file
		if file.stem != TEMPLATE_FILE and file.suffix == ".json":

			# Get the service, constraint name, operator and value
			service, constraint_name, constraint_values = parse_policy(file)

			# Add rule in the dictionary
			if service not in resources_limits:
				resources_limits[service]={}
			resources_limits[service][constraint_name] = constraint_values

	return resources_limits


def build_requested_constraints(request: dict) -> dict[str, dict[str, Constraint]]:
	"""
	Parse received dictionary containing requested constraints
	and build a similar-format dictionary as build_limitations
	to compare request // limitations.

	:param request:
	:return: dict
        Structure of the form
        {
            "navigation": {
                "latency": Constraint(...),
                "frequency": Constraint(...)
            },
            ...
        }
	"""
	resources_request = {}

	try:
		# Extract the relevant service
		uid = request["uid"]
		service = uid.rsplit(":",1)[-1]

		# Parse all asked resources
		for requested_constraint in request["duty"]["constraint"]:

			# Get the service, constraint name, operator and value
			constraint = requested_constraint["leftOperand"].rsplit(":",1)[-1]
			constraint_values = Constraint(
				requested_constraint["operator"],
				parse_value(requested_constraint["rightOperand"])
			)

			# Add in the dictionary
			if service not in resources_request:
				resources_request[service] = {}
			resources_request[service][constraint] = constraint_values
	except KeyError as e:
		raise ValueError(f"Invalid request: {request}") from e

	return resources_request


def compare_constraints(req_val,lim_val,req_ope,lim_ope) -> bool:
	result1=False
	result2=False
	match req_ope :
		case "eq" :
			result1 = (lim_val == req_val)
		case "lt" :
			result1 = (lim_val < req_val)
		case "lteq" :
			result1 = (lim_val <= req_val)
		case "gt" :
			result1 = (lim_val > req_val)
		case "gteq" :
			result1 = (lim_val >= req_val)
	match lim_ope :
		case "eq" :
			result2 = (req_val == lim_val)
		case "lt" :
			result2 = (req_val < lim_val)
		case "lteq" :
			result2 = (req_val <= lim_val)
		case "gt" :
			result2 = (req_val > lim_val)
		case "gteq" :
			result2 = (req_val >= lim_val)
	return result1 and result2


def evaluate_request(request: dict, limits: dict) -> tuple[bool,Constraint]:
	service = list(request)[0]
	# If no server deliver the service
	if service not in limits:
		return False, None

	# Otherwise, check every constraint, if one is False then
	for asked_constraint in request[service]:
		print(asked_constraint)
		if not compare_constraints(
				request[service][asked_constraint].limit_value,
				limits[service][asked_constraint].limit_value,
				request[service][asked_constraint].operator,
				limits[service][asked_constraint].operator
		):
			return False,asked_constraint
	return True,None
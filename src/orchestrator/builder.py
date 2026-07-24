from models import Constraint
from pathlib import Path

from parser import parse_policy, parse_value
from models import Operator

TEMPLATE_FILE = "templates-check"
POLICY_DIRECTORY = Path("./policies/")
ODRL_FILE_FORMAT = ".json"

def add_constraint(constraints_dico: dict[str, dict[str, Constraint]],
				   service: str,
				   constraint_name: str,
				   constraint_values: Constraint
	) -> dict[str, dict[str, Constraint]]:
	"""Add a constraint to a dictionary of constraints"""
	if service not in constraints_dico:
		constraints_dico[service] = {}
	constraints_dico[service][constraint_name] = constraint_values
	return constraints_dico


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
		if file.stem != TEMPLATE_FILE and file.suffix == ODRL_FILE_FORMAT:

			# Get the service, constraint name, operator and value
			service, constraint_name, constraint_values = parse_policy(file)

			# Add rule in the dictionary
			add_constraint(resources_limits,service,constraint_name,constraint_values)

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
			constraint_name = requested_constraint["leftOperand"].rsplit(":",1)[-1]
			constraint_values = Constraint(
				Operator(requested_constraint["operator"]),
				parse_value(requested_constraint["rightOperand"])
			)

			# Add in the dictionary
			add_constraint(resources_request, service, constraint_name, constraint_values)

	except KeyError as e:
		raise ValueError(f"Invalid request: {request}") from e

	return resources_request

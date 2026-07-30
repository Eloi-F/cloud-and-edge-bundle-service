from models import ConstraintSet, ConstraintValues, OdrlSet
from pathlib import Path

from parser import parse_set_file, parse_set
import logging as log

TEMPLATE_FILE = "templates-check"
POLICY_DIRECTORY = Path("./policies/")
ODRL_FILE_FORMAT = ".json"


def add_constraints(
    accumulator: ConstraintSet,
    service: str,
    constraint_dict: dict[str, ConstraintValues],
) -> None:
    """Add a constraint to a dictionary of constraints"""
    for constraint_name, constraint_values in constraint_dict.items():
        if service not in accumulator:
            accumulator[service] = {}
        accumulator[service][constraint_name] = constraint_values


def build_limitations() -> ConstraintSet:
    """
    Parse all ODRL policy files in policies folder
    and build a ConstraintSet of resource limitations.

    :return: resources_limits
            Structure of the form ConstraintSet
    """
    resources_limits: ConstraintSet = {}

    for file in POLICY_DIRECTORY.iterdir():
        # Open and load every ODRL files except templates file
        if file.stem != TEMPLATE_FILE and file.suffix == ODRL_FILE_FORMAT:
            service, constraint_dict = parse_set_file(file)
            add_constraints(resources_limits, service, constraint_dict)

    log.info("Successfully build orchestrator ConstraintSet limitations.")
    return resources_limits


def build_requested_constraints(request: OdrlSet) -> ConstraintSet:
    """
    Parse received dictionary containing requested constraints
    and build a ConstraintSet to compare request // limitations.

    :param request:
    :return: resources_request
            Structure of the form ConstraintSet
    """
    resources_request: ConstraintSet = {}

    service, constraint_dict = parse_set(request)
    add_constraints(resources_request, service, constraint_dict)

    log.info("Successfully build request ConstraintSet.")
    return resources_request

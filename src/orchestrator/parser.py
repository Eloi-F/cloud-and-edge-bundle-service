from models import ConstraintValues, OdrlSet
from pathlib import Path


def parse_policy_file(policy_file: Path) -> tuple[str, dict[str, ConstraintValues]]:
    policy = OdrlSet.model_validate_json(policy_file.read_text(encoding="utf-8"))
    return parse_policy(policy)


def parse_policy(policy: OdrlSet) -> tuple[str, dict[str, ConstraintValues]]:
    """
    Parse a given policy file and return associated
    service and a dict of its constraints.

    :param policy:
    :return: tuple(service,constraint_dict)
    """
    constraint_dict: dict[str, ConstraintValues] = {}

    service = policy.duty.assignee.rsplit(":", 1)[-1]

    for constraint in policy.duty.constraint:
        # Parse constraint name
        constraint_name = constraint.leftOperand.rsplit(":", 1)[-1]

        constraint_dict[constraint_name] = ConstraintValues(
            constraint.operator, constraint.rightOperand
        )

    return service, constraint_dict

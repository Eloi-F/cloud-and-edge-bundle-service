from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel, Field


Operand = int | float | bool


class Operator(Enum):
    EQ = "eq"
    LT = "lt"
    LTEQ = "lteq"
    GT = "gt"
    GTEQ = "gteq"


@dataclass(frozen=True)
class ConstraintValues:
    """
    Represents the values describing an ODRL constraint :
    (operator, operand)
    """

    operator: Operator
    value: Operand


type ConstraintSet = dict[str, dict[str, ConstraintValues]]
"""
A typed dictionary of constraints indexed by services.
Structure of the form
	{
		"service1": {
			"constraint1": (operator, operand),
			"constraint2": (operator, operand),
		}
		"service2": {...},
		...
	}
"""


class OdrlConstraint(BaseModel):
    leftOperand: str
    operator: Operator
    rightOperand: Operand
    comment: str | None = None


class OdrlDuty(BaseModel):
    assignee: str
    target: str
    action: str
    comment: str | None = None
    constraint: list[OdrlConstraint]


class OdrlPolicy(BaseModel):
    """
    Pydantic model to check correct format of incoming ODRL policies.
    """

    context: str = Field(alias="@context")
    type: str = Field(alias="@type")
    uid: str
    duty: OdrlDuty

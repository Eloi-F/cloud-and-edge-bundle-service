from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel


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


type OfferSet = dict[str, dict[str, ConstraintValues]]
"""
A typed dictionary of offered services by a server
	{
		"service1": {
			"metric1": (operator, operand),
			"metric2": (operator, operand),
		}
		"service2": {...},
		...
	}
"""

# Pydantic models

class OdrlConstraint(BaseModel):
	leftOperand: str
	operator: Operator
	rightOperand: Operand
	unit: str | None = None
	comment: str | None = None

class OdrlRule(BaseModel):
	assignee: str
	target: str
	action: str
	constraints: list[OdrlConstraint] | None = None
	comment: str | None = None

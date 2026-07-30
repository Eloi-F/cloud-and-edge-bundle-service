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


class OdrlSet(BaseModel):
	"""
	Pydantic model to check correct format of incoming ODRL Sets from cars.
	"""
	context: str = Field(alias="@context")
	type: str = Field(alias="@type")
	uid: str
	duty: OdrlRule

class OdrlOffer(BaseModel):
	context: str = Field(alias="@context")
	type: str = Field(alias="@type")
	uid: str
	assigner: str
	permission: list[OdrlRule]
	obligation: list[OdrlRule]

class OdrlGraph(BaseModel):
	"""
	Pydantic model to check correct format of incoming ODRL Offers from servers.
	"""
	context: str = Field(alias="@context")
	graph: list[OdrlOffer] = Field(alias="@graph")

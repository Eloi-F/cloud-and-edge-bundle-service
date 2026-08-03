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

type RequestSet = dict[str, dict[str, ConstraintValues]]
"""
A typed dictionary representing a client request.
Used to find the most appropriate server offering
what the client seeks.
(Same type as OfferSet)
	{
		"service1": {
			"metric1": (operator, operand),
			"metric2": (operator, operand),
		}
		"service2": {...},
		...
	}
"""

type ServerOfferSet = dict[str, dict[str, ConstraintValues]]
"""
A typed dictionary of offered services by a server.
	{
		"service1": {
			"metric1": (operator, operand),
			"metric2": (operator, operand),
		}
		"service2": {...},
		...
	}
"""

type OrchestratorOfferSet = dict[str, ServerOfferSet]
"""
A typed dictionary of all offered services by a server
that the orchestrator can distribute to any client.
	{
		"server1": ServerOfferSet1,
		"server2": ServerOfferSet2,
		...
	}
"""

type OfferingServerDict = dict[str, str]
"""
A typed dictionary of all server connected to the 
orchestrator and offering services.
	{
		"server1-id":"server1-url",
		"server2-id":"server2-url",
		...
	}  
"""

# Pydantic models

class BaseOdrlModel(BaseModel):
	"""Common type for ODRL requests and agreements"""
	context: str = Field(alias="@context")
	uid: str
	permission: list[OdrlRule]
	obligation: list[OdrlRule]

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
	constraint: list[OdrlConstraint] | None = None
	comment: str | None = None
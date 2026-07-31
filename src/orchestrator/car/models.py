from common.models import (
	OdrlRule,
	ConstraintValues
)
from typing import Literal
from pydantic import Field, BaseModel

class OdrlAgreement(BaseModel):
	"""
	Pydantic model of incoming ODRL Request from cars.
	"""
	context: str = Field(alias="@context")
	type: Literal["Agreement"] = Field(alias="@type")
	uid: str
	permission: list[OdrlRule]
	obligation: list[OdrlRule]

class OdrlRequest(BaseModel):
	"""
	Pydantic model of incoming ODRL Request from cars.
	"""
	context: str = Field(alias="@context")
	type: Literal["Request"] = Field(alias="@type")
	uid: str
	permission: list[OdrlRule]
	obligation: list[OdrlRule]

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
from src.orchestrator.common.models import (
	OdrlRule,
	ConstraintValues
)
from typing import Literal
from pydantic import Field, BaseModel


class OdrlOffer(BaseModel):
	context: str = Field(alias="@context")
	type: Literal["Offer"] = Field(alias="@type")
	uid: str
	assigner: str
	permission: list[OdrlRule]
	obligation: list[OdrlRule]

class OdrlGraph(BaseModel):
	"""
	Pydantic model of incoming ODRL Offers from servers.
	"""
	context: str = Field(alias="@context")
	graph: list[OdrlOffer] = Field(alias="@graph")

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
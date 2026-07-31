from common.models import OdrlRule
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

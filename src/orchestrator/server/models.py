from common.models import BaseOdrlModel
from typing import Literal
from pydantic import Field, BaseModel


class OdrlOffer(BaseOdrlModel):
	type: Literal["Offer"] = Field(alias="@type")
	assigner: str

class OdrlGraph(BaseModel):
	"""Pydantic model of incoming ODRL offers from servers."""
	context: str = Field(alias="@context")
	graph: list[OdrlOffer] = Field(alias="@graph")

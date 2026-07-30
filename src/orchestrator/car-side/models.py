from src.orchestrator.common.models import (
	OdrlRule,
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
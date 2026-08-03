from common.models import OdrlRule
from typing import Literal
from pydantic import Field, BaseModel

class BaseOdrlModel(BaseModel):
	"""Common type for ODRL requests and agreements"""
	context: str = Field(alias="@context")
	uid: str
	permission: list[OdrlRule]
	obligation: list[OdrlRule]

class OdrlAgreement(BaseOdrlModel):
	"""Pydantic model of outgoing ODRL agreements from orchestrator."""
	type: Literal["Agreement"] = Field(alias="@type")


class OdrlRequest(BaseOdrlModel):
	"""Pydantic model of incoming ODRL request from cars."""
	type: Literal["Request"] = Field(alias="@type")

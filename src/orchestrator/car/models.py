from common.models import BaseOdrlModel
from typing import Literal
from pydantic import Field


class OdrlAgreement(BaseOdrlModel):
	"""Pydantic model of outgoing ODRL agreements from orchestrator."""
	type: Literal["Agreement"] = Field(alias="@type")


class OdrlRequest(BaseOdrlModel):
	"""Pydantic model of incoming ODRL request from cars."""
	type: Literal["Request"] = Field(alias="@type")

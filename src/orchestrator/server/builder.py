import asyncio

from models import (
	OfferingServerDict,
	OrchestratorOfferSet,
	ServerOfferSet
)

def discover_topology() -> tuple[OrchestratorOfferSet, asyncio.Lock, OfferingServerDict, asyncio.Lock]:
	"""
	TO BE DONE: Initialization of two dictionaries:
	- OrchestratorOfferSet : store for each server
	what it can offer and under which conditions
	- OfferingServerDict : keep trace of every
	server offering services
	Use a heartbeat approach.
	:return: OFFERS, OFFERS_LOCKER, SERVERS, SERVERS_LOCKER
	"""
	return {}, asyncio.Lock(), {}, asyncio.Lock()

async def add_server(
		server_dict: OfferingServerDict,
		locker: asyncio.Lock,
		server_id:str,
		server_url:str
	) -> OfferingServerDict :
	"""
	Add a new server to the list of current
	servers able to offer services.

	:param server_dict:
	:param locker:
	:param server_id:
	:param server_url:
	:return: server_dict
	"""
	async with locker:
		server_dict[server_id] = server_url
	return server_dict

async def add_offer(
		offer_dict: OrchestratorOfferSet,
		locker: asyncio.Lock,
		server: str,
		offer: ServerOfferSet
	) -> OrchestratorOfferSet :
	"""
	Add what the new server offers as services
	in the global OrchestratorOfferSet variable.

	:param offer_dict:
	:param locker:
	:param server:
	:param offer:
	:return:
	"""
	async with locker:
		offer_dict[server] = offer
	return offer_dict
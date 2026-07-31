import asyncio

from common.models import (
	OfferingServerDict,
	OrchestratorOfferSet,
	ServerOfferSet
)

import logging
logger = logging.getLogger(__name__)

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
	logger.info(f"Connection to available servers complete.")
	return {}, asyncio.Lock(), {}, asyncio.Lock()


async def add_server(
		server_dict: OfferingServerDict,
		server_id:str,
		server_url:str
	) -> OfferingServerDict :
	"""
	Add a new server to the list of current
	servers able to offer services.

	:param server_dict:
	:param server_id:
	:param server_url:
	:return: server_dict
	"""
	server_dict[server_id] = server_url

	logger.info(f"Added %s (%s) to current servers offering host services register.", server_id, server_url)
	return server_dict


async def add_offer(
		offer_dict: OrchestratorOfferSet,
		server_id: str,
		offer: ServerOfferSet
	) -> OrchestratorOfferSet :
	"""
	Add what the new server offers as services
	in the global OrchestratorOfferSet variable.

	:param offer_dict:
	:param server_id:
	:param offer:
	:return:
	"""
	offer_dict[server_id] = offer

	logger.info(f"Added %s's offer to overall offers register.",server_id)
	return offer_dict

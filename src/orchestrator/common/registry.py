from models import (
	OrchestratorOfferSet,
	OfferingServerDict,
	ServerOfferSet,
	RequestSet
)
import asyncio
from evaluator import compare_constraints

import logging
logger = logging.getLogger(__name__)


class TopologyRegistry:
	"""

	"""

	offers:         OrchestratorOfferSet
	offers_locker:  asyncio.Lock
	servers:        OfferingServerDict
	servers_locker: asyncio.Lock

	def __init__(self):
		"""
		TO BE DONE: Initialization of two dictionaries:
		- OrchestratorOfferSet : store for each server
		what it can offer and under which conditions
		- OfferingServerDict : keep trace of every
		server offering services
		Use a heartbeat approach.
		"""
		logger.info("Connection to available servers complete.")
		self.offers = {}
		self.offers_locker = asyncio.Lock()
		self.servers = {}
		self.servers_locker = asyncio.Lock()


	async def lock_offers(self):
		"""Lock offers locker. To be called before using offers variable"""
		await self.offers_locker.acquire()

	async def unlock_offers(self):
		"""Unlock offers locker. To be called after using offers variable"""
		self.offers_locker.release()

	async def lock_servers(self):
		"""Lock servers locker. To be called before using servers variable"""
		await self.servers_locker.acquire()

	async def unlock_servers(self):
		"""Unlock servers locker. To be called after using servers variable"""
		self.servers_locker.release()


	async def register_server(self, server_id: str, server_url: str):
		"""Add a new server to the dict of current servers able to offer services."""
		await self.lock_servers()
		self.servers[server_id] = server_url
		await self.unlock_servers()
		logger.info(f"Added %s (%s) to current connected servers register.", server_id, server_url)


	async def register_offer(self,server_id: str,offer: ServerOfferSet):
		"""Add an offer from a new server to the dict of all available host services offers."""
		await self.lock_offers()
		self.offers[server_id] = offer
		await self.unlock_offers()
		logger.info(f"Added %s's offer to overall offers register.", server_id)


	def check_capable_server(
			self,
	        server: str,
			request: RequestSet
	) -> bool:
		"""
		Check if a server is able to handle needs of a
		client request based on the metrics it proposes.
		/!\ SHOULD BE CALLED FROM AN ASYNC FUNCTION.
		check_capable_server assume that self.servers
		is already protected by the locker.

		:param server:
		:param request:
		:return: bool
		"""
		service: str = list(request)[0]

		# Check only if they propose the service
		if not service in self.offers[server] : return False

		# Check every metric asked by the client
		for metric in request[service]:
			include = metric in self.offers[server][service]
			logger.debug("Checking whether %s is in %s : %s",
			             metric, self.offers[server][service], include)
			if not (include and compare_constraints(
					request[service][metric],
					self.offers[server][service][metric]
			)):
				logger.debug("-> Server is not capable to handle client needs.")
				return False
		logger.debug("-> Server is capable to handle client needs.")
		return True


	async def build_capable_servers(
			self,
			request_set: RequestSet,
	) -> OrchestratorOfferSet:
		"""
		Build a dict of all servers capable to handle
		needs of a client request, in order to find
		the most suitable one.

		:param request_set:
		:return: OrchestratorOfferSet
		"""

		result: OrchestratorOfferSet = {}
		await self.lock_offers()

		# Browse all available servers
		for server in self.offers.keys():
			if self.check_capable_server(server, request_set):
				result[server] = self.offers[server]

		await self.unlock_offers()

		logger.info("Built dict of servers capable of handling client request.")
		return result


	async def most_suitable_server(self):
		pass
import logging
logger = logging.getLogger(__name__)

def calculate_speed(dist: float, cliff_state: bool):
	"""
	Returns speed percentage to adopt, based on linear
	formula.

	:param dist: Distance to the obstacle
	:param cliff_state: True if a cliff is detected ahead, otherwise False
	:return float: Speed percentage to apply
	"""

	if cliff_state or dist <= 10:
		logger.debug("Computing speed : cliff ahead, returning 0.")
		return 0
	elif dist >= 90:
		logger.debug("Computing speed : clear road, returning 100.")
		return 100
	else:
		# f : dist ∈ [10;90] |---> [0;100]
		logger.debug("Computing speed : obstacle ahead, slowing down.")
		return 1.25 * dist - 12.5

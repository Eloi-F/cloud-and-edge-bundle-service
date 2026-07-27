from models import ConstraintValues, Operator, Operand, ConstraintSet
from math import inf
from dataclasses import dataclass


@dataclass(frozen=True)
class Interval:
	"""
	Represent an interval for constraint comparison.
	Simplify handling
	"""
	lower_value: float
	lower_inclusive: bool
	upper_value: float
	upper_inclusive: bool

	def lower_key(self) -> tuple[float, int]:
		"""Transform a lower value into a tuple (value, epsilon),
		where epsilon shows whether the value is reachable or not"""
		return self.lower_value , 0 if self.lower_inclusive else 1

	def upper_key(self) -> tuple[float, int]:
		"""Transform an upper value into a tuple (value, epsilon),
		where epsilon shows whether the value is reachable or not"""
		return self.upper_value , 0 if self.upper_inclusive else -1

	def overlaps(self, other: "Interval") -> bool:
		"""True if the two intervals share at least a common value."""
		return self.lower_key() <= other.upper_key() and other.lower_key() <= self.upper_key()



def to_interval(value: Operand, operator: Operator) -> Interval:
	"""Transform a value and an operator into an open interval for constraint comparison."""

	# First, check whether val is float or int
	if not isinstance(value, int) and not isinstance(value, float):
		raise ValueError(f"Semantic error : impossible to transform {type(value)} typed value to an interval.")

	# Transform given values into an interval
	match operator:
		case Operator.LTEQ :    return Interval(0, True, value, True)
		case Operator.LT :      return Interval(0, True, value, False)
		case Operator.GTEQ :    return Interval(value, True, inf, True)
		case Operator.GT : 	    return Interval(value, False, inf, True)
		case Operator.EQ:       return Interval(value, True, value, True)


def compare_constraints(req_constraint: ConstraintValues, orch_constraint: ConstraintValues) -> bool:
	"""
	Checks whether the requested value is within the allowed range
	given by orchestrator ODRL policies.
	:param orch_constraint:
	:param req_constraint:
	:return: bool
	"""
	req_interval = to_interval(
		req_constraint.value,
		req_constraint.operator
	)
	orch_interval = to_interval(
		orch_constraint.value,
		orch_constraint.operator
	)
	return req_interval.overlaps(orch_interval)


def evaluate_request(request: ConstraintSet, limits: ConstraintSet) -> tuple[bool, list[ConstraintValues] | None]:
	"""
	Compare and tell if the request matches with current limitations.
	If it does not, return the impossible constraints.
	:param request:
	:param limits:
	:return: tuple[bool, ConstraintValues | None]
	"""
	# Only one service per request
	service = list(request)[0]

	# If no server deliver the service
	if service not in limits:
		return False, None

	ok = True
	impossible_constraints = []

	# Otherwise, check every constraint, if one is False then return false
	for constraint_name in request[service]:
		if not compare_constraints(request[service][constraint_name],limits[service][constraint_name]):
			ok = False
			impossible_constraints.append(request[service][constraint_name])
	if not ok :
		return False,impossible_constraints
	return True,None
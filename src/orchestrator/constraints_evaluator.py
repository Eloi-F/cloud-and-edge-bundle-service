from models import Constraint, Operator, Operand


def compare_constraints(
		req_val: Operand,
		lim_val: Operand,
		req_ope: Operator,
		lim_ope: Operator
	) -> bool:
	result1=False
	result2=False
	match req_ope :
		case Operator.EQ :
			result1 = (lim_val == req_val)
		case Operator.LT :
			result1 = (lim_val < req_val)
		case Operator.LTEQ :
			result1 = (lim_val <= req_val)
		case Operator.GT :
			result1 = (lim_val > req_val)
		case Operator.GTEQ :
			result1 = (lim_val >= req_val)
	match lim_ope :
		case Operator.EQ:
			result2 = (req_val == lim_val)
		case Operator.LT :
			result2 = (req_val < lim_val)
		case Operator.LTEQ :
			result2 = (req_val <= lim_val)
		case Operator.GT :
			result2 = (req_val > lim_val)
		case Operator.GTEQ :
			result2 = (req_val >= lim_val)
	return result1 and result2


def evaluate_request(request: dict, limits: dict) -> tuple[bool,Constraint]:
	service = list(request)[0]
	# If no server deliver the service
	if service not in limits:
		return False, None

	# Otherwise, check every constraint, if one is False then
	for asked_constraint in request[service]:
		print(asked_constraint)
		if not compare_constraints(
				request[service][asked_constraint].limit_value,
				limits[service][asked_constraint].limit_value,
				request[service][asked_constraint].operator,
				limits[service][asked_constraint].operator
		):
			return False,asked_constraint
	return True,None
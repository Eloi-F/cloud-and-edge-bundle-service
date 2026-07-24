from dataclasses import dataclass
from enum import Enum

Operand = int | float | bool | str

class Operator(Enum):
	EQ = 'eq'
	LT = 'lt'
	LTEQ = 'lteq'
	GT = 'gt'
	GTEQ = 'gteq'

@dataclass(frozen=True)
class Constraint:
	operator: Operator
	limit_value: Operand

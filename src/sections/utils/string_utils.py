
from typing import Iterable

def trunc_string(string:str, size:int) -> str:
	""" tronque la stirng pour quelle fasse size """
	if len(string) <= size:
		return string
	return f'{string[:size - 2]}..'

def get_equal_string(span:int) -> str:
	""" return la chaine de char contenant le egal avec ou sans espace autour """
	return '{:^{size}}'.format('=', size=between(1, span + 1, 3))

def between(lower_bound:int, value:int, upper_bound:int) -> int:
	""" retourne le max/min de value entre lower_bound et upper_bound """
	return max(lower_bound, min(value, upper_bound))

def join_lines(lines:Iterable[str], sep:str='║') -> str:
	""" join the lines with a | character """
	return sep.join(lines) + sep

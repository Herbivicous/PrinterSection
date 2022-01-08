
from typing import Any

from src.sections.Element import AbstractElement, Iterator, ElementLine

class StubElement(AbstractElement):

	def iter_lines(self, data:Any, span:int) -> Iterator[ElementLine]:
		yield ElementLine(span*'@')

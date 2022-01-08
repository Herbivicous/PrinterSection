
from src.sections.Element import AbstractElement, Iterator, ElementLine

class StubElement(AbstractElement):

	def iter_lines(self, span:int) -> Iterator[ElementLine]:
		yield ElementLine(span*'@')

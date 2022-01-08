
from abc import ABC, abstractmethod
from typing import Iterator, List, Any
from itertools import repeat

from .Element import AbstractElement #, Numeric, Bool, Title,Sep

class AbstractSection(ABC):
	""" an abstract section """

	@abstractmethod
	def lines(self, data:Any, span:int) -> Iterator[str]:
		""" iterator over the lines of its elements """

class Section(AbstractSection):
	""" Une section de printer """

	def __init__(self, *elements:AbstractElement):
		self.elements:List[AbstractElement] = list(elements)

	def lines(self, data:Any, span:int) -> Iterator[str]:

		for element in self.elements:
			yield from element.lines(data, span)

		yield from repeat(span*' ')

	def add(self, *element:AbstractElement):
		""" adds a new element to the section """
		self.elements.extend(element)

# def section_from_dataclass(data_object):
# 	assert hasattr(data_object, '__dataclass_fields__'), 'data_object is not a dataclass'
# 	section = Section()

# 	section.add(Title(data_object.__class__.__name__))
# 	section.add(Sep())

# 	for field in data_object.__dataclass_fields__.values():
# 		section.add(element_from_field(data_object, field))

# 	return section

# def element_from_field(data_object, field) -> AbstractElement:
# 	if issubclass(field.type, bool):
# 		return Bool(lambda:getattr(data_object, field.name), name=field.name)
# 	if issubclass(field.type, int):
# 		return Numeric(lambda:getattr(data_object, field.name), name=field.name)

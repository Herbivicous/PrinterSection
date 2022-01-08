
from unittest import TestCase
from unittest.mock import Mock

from src.sections.Section import Section

from .stubs.StubElement import StubElement

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=no-self-use

class TestSection(TestCase):

	def test_empty_init(self):
		section = Section()

		assert len(section.elements) == 0

	def test_init(self):
		section = Section(Mock(), Mock(), Mock())

		assert len(section.elements) == 3

	def test_add(self):
		section = Section()
		section.add(Mock(), Mock(), Mock())

		assert len(section.elements) == 3

	def test_empty_lines(self):
		section = Section()

		assert len(next(section.lines(5))) == 5
		assert next(section.lines(5)) == '     '

	def test_lines(self):
		element = StubElement()
		section = Section(element)

		lines = section.lines(5)
		assert next(lines) == '@@@@@'
		assert next(lines) == '     '

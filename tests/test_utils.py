
from src.sections.utils.printer_utils import horizontal_border

# pylint: disable=no-self-use

class TestHorizontalBorder:
	""" tests for the horizontal_border function """

	def test_not_top_border(self):
		""" horizontal_border should have crosses when not top border """
		assert horizontal_border(5, 5, False) == '═════╬═════╬═════╬═════╬═════╣'

	def test_top_border(self):
		""" horizontal_border top side should be flat if top border """
		assert horizontal_border(5, 5, True) == '═════╦═════╦═════╦═════╦═════╗'

	def test_fewer_sections(self):
		""" horizontal_border should have the correct number of section """
		assert horizontal_border(5, 2, True) == '═════╦═════╗'

	def test_smaller_sections(self):
		""" horizontal_border should have the correct section size """
		assert horizontal_border(2, 5, True) == '══╦══╦══╦══╦══╗'

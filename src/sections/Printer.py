
from typing import Tuple, Dict, Optional, Iterator, List, Any
from itertools import repeat

from .Section import AbstractSection
from .CoordinatesManager import CoordinatesManager, Coordinates

from .utils.printer_utils import horizontal_border, get_screen_size
from .utils.string_utils import join_lines

Dimensions = Tuple[int, int]

class Printer:
	""" gestion d'un printer, compose de plusieurs sections """
	def __init__(
		self,
		screen_dimensions:Dimensions,
		coordinates:CoordinatesManager,
		stream
	):
		self.sections : Dict[Tuple[int, int], AbstractSection] = {}

		self.number_of_section_per_row, self.number_of_section_per_column = coordinates.dimensions
		self.screen_width,               self.screen_height                = screen_dimensions

		self.coordinates = coordinates

		self.stream = stream

	@classmethod
	def create(cls, cols:int, rows:int):
		from sys import stdout
		return cls(get_screen_size(), CoordinatesManager(cols, rows), stdout)

	@property
	def section_width(self) -> int:
		""" returns the width of a section"""
		return self.screen_width // self.number_of_section_per_row - 1

	@property
	def section_height(self) -> int:
		""" returns the height of a section"""
		return self.screen_height // self.number_of_section_per_column - 1

	def add_section(self, section:AbstractSection, data:Any, coordinates:Optional[Coordinates]=None):
		""" ajoute une section au coordonnees si donnees, sinon a une case libre """
		if coordinates:
			if self.coordinates and coordinates in self.coordinates:
				self.coordinates.remove(coordinates)
		else:
			coordinates = self.coordinates.get_available()

		self.sections[coordinates] = (section, data)

	# def __inputs_iter(self):
	# 	return cycle(chain(*[section.inputs_iter() for section in self.sections.values()]))

	def print(self):
		""" prints """
		self.stream.write('\033[0;0H')
		self.stream.write('\n'.join(self.lines()))
		self.stream.flush()

	def lines(self) -> Iterator[str]:
		""" yields all the lines """

		for section_row_index in range(self.number_of_section_per_column):

			yield horizontal_border(
				self.section_width, self.number_of_section_per_row, section_row_index == 0
			)

			yield from self.section_lines(section_row_index)

	def section_lines(self, section_row_index:int) -> Iterator[str]:
		""" yields the lines of the sections to be displayed """

		line_iterators = self.build_line_iters(section_row_index)

		for line_index, line in enumerate(zip(*line_iterators)):

			yield join_lines(line)

			if line_index >= self.section_height - 1:
				return

	def build_line_iters(self, section_row_index:int) -> List[Iterator[str]]:
		""" build a list of iterator from the row's section lines iterator """
		line_iterators = []
		for section_column_index in range(self.number_of_section_per_row):

			if (section_column_index, section_row_index) in self.sections:

				section, data = self.sections[(section_column_index, section_row_index)]
				line_iterators.append(section.lines(data, self.section_width))
			else:
				line_iterators.append(repeat(' '*self.section_width))

		return line_iterators

	def restore(self):
		""" restaure l'affichage de l'invite de commande, marche pas trop """
		self.stream.write('\033[?25h')
		self.stream.flush()

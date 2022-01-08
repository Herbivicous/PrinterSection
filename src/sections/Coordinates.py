
from typing import Tuple, Set

Coordinates = Tuple[int, int]

class CoordinatesManager:

	def __init__(self, cols:int, rows:int):
		self.cols = cols
		self.rows = rows
		self.available_coordinates:Set[Coordinates] = {
			(x, y) for y in range(rows) for x in range(cols)
		}

	def get_available(self) -> Coordinates:
		""" returns a tuple of avaible coordinates """
		return self.available_coordinates.pop()

	def remove(self, coordinates:Coordinates) -> None:
		""" remove the coordinates from the available """
		self.available_coordinates.remove(coordinates)

	def __iter__(self):
		return self.available_coordinates.__iter__()

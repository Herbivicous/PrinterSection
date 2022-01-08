
from unittest import TestCase

from src.sections.CoordinatesManager import CoordinatesManager

class TestCoordinatesManager(TestCase):

	def test_length(self):

		manager = CoordinatesManager(31, 19)

		assert len(manager.available_coordinates) == 31 * 19
		assert len(manager.available_coordinates) == len(set(manager.available_coordinates))

	def test_get_coords(self):

		manager = CoordinatesManager(31, 19)

		x, y = manager.get_available()

		assert 0 <= x < 31
		assert 0 <= y < 19
		assert len(set(manager.available_coordinates)) == 31 * 19 - 1

	def test_get_first_coords_first(self):

		manager = CoordinatesManager(31, 19)

		x, y = manager.get_available()

		assert (x, y) == (0, 0)

	def test_empty_manager(self):

		manager = CoordinatesManager(1, 2)

		manager.get_available()
		manager.get_available()

		self.assertRaises(IndexError, manager.get_available)


from sys import stdout
from random import random, randint
from time import sleep

from typing import List
from dataclasses import dataclass

from src.sections.Printer import Printer
from src.sections.Section import Section
from src.sections.Element import Title, Text, Sep, Bool, Ratio, Numeric, Bar, Str 
from src.sections.ElementStyle import ElementStyle as Style
from src.sections.utils.printer_utils import get_screen_size

from src.sections.Coordinates import CoordinatesManager

@dataclass
class Test:
	""" a random object """

	value:int=0
	is_closed:bool=True
	ratio = (0, 0)
	progress:float=0

	def randomize(self):
		self.value = randint(0, 9999999)
		self.is_closed = bool(randint(0, 1))
		self.ratio = (randint(0, 100), randint(1, 100))
		self.progress = round(100*random(), 2)

test = Test()

printer = Printer((2, 2), get_screen_size(), CoordinatesManager(2, 2), stdout)
printer.add_section(
	Section(
		Title('title'),
		Text('hello', Style(color='red')),
		Sep(),
		Bool(lambda:test.is_closed, 'Closed'),
		Ratio(lambda:test.ratio, 'done', Style(color='red', align='>')),
		Numeric(lambda:test.value, 'value', 'kg', Style(color='green')),
		Numeric(lambda:test.progress, '', '%', Style(color='green', align='^')),
		Bar(lambda:test.progress/100, 'Progress', Style(color='red')),
	)
)
printer.add_section(
	Section(
		Str(lambda:[34, 35, 75][randint(0, 2)]*"@", 'done'),
	)
)

for _ in range(5):
	printer.print()
	test.randomize()
	sleep(0.5)

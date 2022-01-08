
from random import random, randint
from time import sleep

from typing import List
from dataclasses import dataclass

from src.sections.Printer import Printer
from src.sections.Section import Section
from src.sections.Element import Title, Text, Sep, Bool, Ratio, Numeric, Bar, Str 
from src.sections.Style import Style

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

test1 = Test()
test2 = Test()

printer = Printer.create(2, 2)
section = Section(
	Title('title'),
	Text('hello', Style(color='red')),
	Sep(),
	Bool(lambda x:x.is_closed, 'Closed'),
	Ratio(lambda x:x.ratio, 'done', Style(color='red', align='>')),
	Numeric(lambda x:x.value, 'value', 'kg', Style(color='green')),
	Numeric(lambda x:x.progress, '', '%', Style(color='green', align='^')),
	Bar(lambda x:x.progress/100, 'Progress', Style(color='red')),
)

printer.add_section(section, test1)
printer.add_section(section, test2)
printer.add_section(Section.from_dataclass(Test), test1)
# printer.add_section(
# 	Section(
# 		Str(lambda:[34, 35, 75][randint(0, 2)]*"@", 'done'),
# 	)
# )

for _ in range(5):
	printer.print()
	test1.randomize()
	test2.randomize()
	sleep(0.5)


from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterator, Callable, Any, List, Optional

from .Style import Style
from .ElementLine import ElementLine

from .utils.string_utils import trunc_string, get_equal_string, between

PropertyAccessor = Callable[[], Any]


class AbstractElement(ABC):

	style:Optional[Style]=None

	def lines(self, data:Any, span:int) -> Iterator[str]:
		""" generator over the styled lines of the element """

		for line in self.iter_lines(data, span):
			if self.style:
				yield self.style.apply(line, span)
			else:
				yield line.value

	@abstractmethod
	def iter_lines(self, data:Any, span:int) -> Iterator[ElementLine]:
		""" generator over the lines of the element """

@dataclass
class Sep(AbstractElement):
	""" une ligne de separation """

	sep_char:str='─'
	style:Style = Style()

	def iter_lines(self, data:Any, span:int) -> Iterator[ElementLine]:
		yield ElementLine(span*self.sep_char)

@dataclass
class Text(AbstractElement):
	""" une string constante """

	text:str=''
	style:Style = Style()

	def iter_lines(self, data:Any, span:int) -> Iterator[ElementLine]:
		yield ElementLine(trunc_string(self.text, span))

@dataclass
class Title(AbstractElement):
	""" le titre d'une section """

	text:str=''
	style:Style = Style(align='^', strf='upper')

	def iter_lines(self, data:Any, span:int) -> Iterator[ElementLine]:
		yield ElementLine(trunc_string(self.text, span))

@dataclass
class Bool(AbstractElement):
	""" un booleen, represente par une case a cocher """

	accessor:PropertyAccessor
	name:str=''
	style:Style = Style()

	def iter_lines(self, data:Any, span:int) -> Iterator[ElementLine]:
		value = '■' if self.accessor(data) else ' '
		template = trunc_string(self.name, span - 3) + '[{}]'
		yield ElementLine(value, template)

@dataclass
class Numeric(AbstractElement):
	""" une unite, similaire a int mais affiche param a la fin """

	accessor:PropertyAccessor
	name:str=''
	unit:str=''
	style:Style = Style()

	def iter_lines(self, data:Any, span:int) -> Iterator[ElementLine]:
		value = str(self.accessor(data))
		yield ElementLine(f'{value}{self.unit}', self.template(span, value))

	def template(self, span:int, value:str) -> str:
		""" returns the template for the numeric """
		if self.name:
			max_used_length = len(self.name) + len(value) + 1 + len(self.unit)
			equal_string = get_equal_string(span - max_used_length)
			remaining_length = span - len(self.unit) - len(value) - len(equal_string)
			name = trunc_string(self.name, remaining_length)
			return f'{name}{equal_string}{{}}'
		return '{}'

@dataclass
class Bar(AbstractElement):
	""" une bar de progression """

	accessor:PropertyAccessor
	name:str=''
	style:Style = Style()
	filler:str=' '

	def iter_lines(self, data:Any, span:int) -> Iterator[ElementLine]:

		total_length = (span - len(self.name) - 2 - int(bool(self.name)))
		progress_chars = round(between(0, self.accessor(data), 1)*total_length)
		progress_bar = f"{progress_chars*'■':{self.filler}<{total_length}}"

		template = self.template(self.name, span)

		yield ElementLine(progress_bar, template)

	@staticmethod
	def template(name:str, span:int) -> str:
		""" return a progress bar template """
		return f'{trunc_string(name, span//2)}:[{{}}]' if name else '[{}]'

@dataclass
class Ratio(AbstractElement):
	""" un ration, la valeur doit etre un tuple (value, max_value) """

	accessor:PropertyAccessor
	name:str=''
	style:Style = Style()

	def iter_lines(self, data:Any, span:int) -> Iterator[ElementLine]:
		value, max_value = self.accessor(data)
		template = self.template(self.name, span, value, max_value)
		yield ElementLine(f'{value}/{max_value}', template)

	@staticmethod
	def template(name:str, span:int, value:int, max_value:int) -> str:
		""" returns a template for a ratio """
		if name:
			name = trunc_string(name, span - 2 - len(str(value)) - len(str(max_value)))
			return f'{name}:{{}}'
		return '{}'

@dataclass
class Str(AbstractElement):
	""" une string """

	accessor:PropertyAccessor
	name:str=''
	style:Style = Style()

	def iter_lines(self, data:Any, span:int) -> Iterator[ElementLine]:
		string = self.accessor(data)
		string_len = len(string)

		if string_len + len(self.name) + 1 > span:
			yield ElementLine('', f'{self.name}:') # yields the name

			if string_len + 2 <= span:
				yield ElementLine(string)
			else:
				yield ElementLine(string[:span - 1])
				i = span-2
				while i + span - 2 < string_len:
					yield ElementLine(string[i:i+span-2], ' {} ')
					i += span - 1
				yield ElementLine(string[i:string_len], ' {}')
		else:
			yield ElementLine(string, f'{self.name}:{{}}')

@dataclass
class Row(AbstractElement):
	""" une ligne d'elements """

	elements:List[AbstractElement]
	sep:str='|'
	style:Style = Style()

	def iter_lines(self, data:Any, span:int) -> Iterator[ElementLine]:
		each_len = span/len(self.elements)
		yield next(map(
			lambda lines: ElementLine(self.sep.join(lines)),
			zip(*(
				element.lines(round((i+1)*each_len)-round(i*each_len))
				for i, element in enumerate(self.elements))
			))
		)

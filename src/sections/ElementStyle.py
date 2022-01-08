
from dataclasses import dataclass
from typing import Optional, Callable, Any

from .ElementLine import ElementLine

from .utils.types import FormattingValues
from .utils.printer_utils import color_formatting_values

@dataclass
class ElementStyle:

	align:str='<'
	color:str=''
	colorf:Optional[Callable[[Any], str]]=None
	hidden:bool=False
	underline:bool=False
	light:bool=False
	strf:str=''

	def get_formatting_values(self) -> FormattingValues:
		""" returns the formatting values associated with the style """
		formatting_values = []

		if self.color:
			formatting_values.extend(color_formatting_values(self.color))

		if self.underline:
			formatting_values.append('4')

		if self.light:
			formatting_values.append('1')

		return formatting_values

	@property
	def styled_template(self) -> str:
		""" return a template string, where .format will be stylized """
		return ''.join(['\033[', ';'.join(self.get_formatting_values()), 'm', '{}', '\033[0m'])

	def apply(self, element:ElementLine, span:int) -> str:
		""" aplly the style to the line """
		if self.hidden:
			return span*' '

		unformatted_string = element.template.format(element.value)
		formatted_string = element.template.format(
			self.styled_template.format(
				getattr(str, self.strf, lambda x:x)(element.value)
			)
		)
		unformatted_padded_string = (
			f'{unformatted_string:{self.align}{span}.{span}}'
		)
		return unformatted_padded_string.replace(unformatted_string, formatted_string)

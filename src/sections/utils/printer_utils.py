
import os
import shutil
from typing import Tuple

from .types import FormattingValues

def get_screen_size() -> Tuple[int, int]:
	""" return the size of the terminal """
	win_size = shutil.get_terminal_size(fallback=(80, 24))
	if win_size:
		width, height = win_size
	else:
		unix_size = os.popen('stty size', 'r').read().split()
		height, width = unix_size
	return (int(width), int(height))

def horizontal_border(border_width:int, number_of_section:int, is_top_border:bool) -> str:
	""" creates and returns the horizontal_border border from the parameter """
	cross_char, last_cross_char = ('╦', '╗') if is_top_border else ('╬', '╣')
	top_border_str = f'{cross_char:═>{border_width+1}}'
	last_top_border_str = f'{last_cross_char:═>{border_width+1}}'
	return f'{(number_of_section-1)*top_border_str}{last_top_border_str}'

FOREGROUND_COLORS = {
	'black': '30',
	'red': '31',
	'green': '32',
	'yellow': '33',
	'blue': '34',
	'magenta': '35',
	'cyan': '36',
	'white': '37',
	'extended': '38',
	'default': '39'
}

def color_formatting_values(color:str) -> FormattingValues:
	""" return the formatting values """

	if color in FOREGROUND_COLORS:
		return [FOREGROUND_COLORS[color]]

	if color[0] == '#' and len(color) == 7:
		return ['38', '2', b10(color[1:3]), b10(color[3:5]), b10(color[5:7])]

	raise ValueError(f"Can't format color {color}")

def b10(b16_number_string:str) -> str:
	""" convert a b16 number into a b10 """
	return str(int(b16_number_string[1:3], 16))

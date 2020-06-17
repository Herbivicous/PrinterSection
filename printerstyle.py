

# pylint: disable=C0330
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

BACKGROUND_COLORS = {
	'black': '40',
	'red': '41',
	'green': '42',
	'yellow': '43',
	'blue': '44',
	'magenta': '45',
	'cyan': '46',
	'white': '47',
	'extended': '48',
	'default': '49'
}

STR_FUNC = {
	'lower': lambda string: str(string).lower(),
	'upper': lambda string: str(string).upper(),
	'title': lambda string: str(string).title(),
	'capitalize': lambda string: str(string).capitalize()
}

class Style:
	""" Une classe style """
	def __init__(self, **kwargs):
		self.kwargs = kwargs
		self.element = None

	def __get_color(self, formatting_values):
		""" retourne la couleur en fonction de la valeur """
		color = False
		if 'colorf' in self.kwargs:
			color = self.kwargs['colorf'](self.element.get_value())
		elif 'color' in self.kwargs:
			color = self.kwargs['color']
		if color:
			formatting_values.append(FOREGROUND_COLORS[color])

	def __get_pos(self):
		if 'pos' in self.kwargs:
			return self.kwargs['pos']
		return '<'

	def __treat_string(self, value):
		if 'strf' in self.kwargs:
			func_code = self.kwargs['strf']
			return STR_FUNC[func_code](value)
		return value

	def styled(self, string, value, n_col):
		""" applique le style a la valeur et la met dans la string """
		formatting_values = []
		self.__get_color(formatting_values)
		value = self.__treat_string(value)
		if self.kwargs.get('underline', False):
			formatting_values.append('4')
		if self.kwargs.get('light', False):
			formatting_values.append('1')

		styled_string = ''.join(['\033[', ';'.join(formatting_values), 'm', '{}', '\033[0m'])
		base_string = string.format(value)
		unpadded_string = string.format(styled_string.format(value))
		pos = self.__get_pos()
		padded_string = '{:{pos}{size}.{size}}'.format(base_string, pos=pos, size=n_col)
		return padded_string.replace(base_string, unpadded_string)

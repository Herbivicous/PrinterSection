""" liste des elements printables """

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

def between(lower_bound, value, upper_bound):
	""" retourne le max/min de value entre lower_bound et upper_bound """
	return max(lower_bound, min(value, upper_bound))

class PrinterElement:
	""" class abstraite pour tous les element printable """
	def __init__(self, obj, style, name=None, display_name=None):
		self.obj = obj
		self.var_name = name
		self.name = display_name if display_name is not None else name
		self.style = style

	def _format(self, string):
		styled_string = string
		formatting_values = []
		if 'color' in self.style:
			formatting_values.append(FOREGROUND_COLORS[self.style['color']])
		if 'background' in self.style:
			formatting_values.append(BACKGROUND_COLORS[self.style['background']])
		if 'letters' in self.style:
			if self.style['letters'] == 'lower':
				styled_string = styled_string.lower()
			if self.style['letters'] == 'upper':
				styled_string = styled_string.upper()
			if self.style['letters'] == 'capital':
				styled_string = styled_string.capitalize()
		if 'underline' in self.style and self.style['underline']:
			formatting_values.append('4')
		if 'bold' in self.style and self.style['bold']:
			formatting_values.append('1')

		return ''.join(['\033[', ';'.join(formatting_values), 'm', styled_string, '\033[0m'])

	def to_string(self, n_col_max):
		""" retourne la string de l'element """
		raise NotImplementedError(":'(")

class PrinterTitle(PrinterElement):
	""" le titre d'une section """
	def to_string(self, n_col_max):
		attr_val = getattr(self.obj, self.var_name)
		raw_string = '{:^{taille}}'.format(attr_val, taille=n_col_max)
		yield self._format(raw_string), n_col_max

class PrinterBool(PrinterElement):
	""" un booleen, represente par une case a cocher """
	def to_string(self, n_col_max):
		if bool(getattr(self.obj, self.var_name)):
			res = '[■]'
		else:
			res = '[ ]'
		if len(self.name) + 3 > n_col_max:
			yield self._format(self.name[:n_col_max - 5] + '..' + res), n_col_max
		else:
			yield self._format(self.name + res), len(self.name) + 3

class PrinterInt(PrinterElement):
	""" un entier """
	def to_string(self, n_col_max):
		name = self.name
		val = str(getattr(self.obj, self.var_name))
		self_len = len(name) + len(val) + 1
		equal = '{:^{size}}'.format('=', size=between(1, n_col_max - self_len + 1, 3))
		res = '{}{}{}'.format(name, equal, val)
		if self_len > n_col_max:
			res = '{}..'.format(res[:n_col_max - 2])
		yield self._format(res), self_len + len(equal) - 1

class PrinterStr(PrinterElement):
	""" une string """
	def to_string(self, n_col_max):
		string = getattr(self.obj, self.var_name)
		string_len = len(string)
		name_len = len(self.name)
		format_f = self._format
		if string_len + name_len + 4 > n_col_max:
			yield format_f('-{}:'.format(self.name)), name_len + 2
			if string_len + 2 <= n_col_max:
				yield format_f('"{}"'.format(string)), string_len + 2
			else:
				yield format_f('"{}'.format(string[:n_col_max - 2])), n_col_max - 1
				i = n_col_max-2
				while i + n_col_max - 2 < string_len:
					yield format_f(' {} '.format(string[i:i+n_col_max-2])), n_col_max
					i += n_col_max - 1
				yield format_f(' {}"'.format(string[i:string_len])), 2 + string_len - i
		else:
			yield format_f('-{}:"{}"'.format(self.name, string)), name_len + string_len + 4

	def __len__(self):
		value = getattr(self.obj, self.var_name)
		return len(self.name) + len(str(value)) + 1

class PrinterSep(PrinterElement):
	""" une ligne de separation """
	def __init__(self, obj, style, char):
		super().__init__(obj, style)
		self.char = char

	def to_string(self, n_col_max):
		yield self._format(n_col_max*self.char), n_col_max

class PrinterBar(PrinterElement):
	def to_string(self, n_col_max):
		val = between(0, getattr(self.obj, self.var_name), 1)
		name = self.name
		total = (n_col_max - len(name) - 3)
		progress = round(val*total)
		left = total - progress
		string_tab = [name, ':[', progress*'■', left*' ', ']']
		yield self._format(''.join(string_tab)), len(name) + 3 + total
		
class PrinterRatio(PrinterElement):
	def to_string(self, n_col_max):
		name = self.name
		val, val_max = getattr(self.obj, self.var_name)
		str_length = 2 + len(name) + len(str(val)) + len(str(val_max))
		if str_length > n_col_max:
			depassement = str_length - n_col_max
			yield self._format('{:.{taille}}..:{}/{}'.format(name, val, val_max, taille=len(name)-depassement-2)), n_col_max
		else:
			yield self._format('{}:{}/{}'.format(name, val, val_max)), str_length

class PrinterStatus(PrinterElement):
	def __init__(self, obj, style, name, display_name, settings):
		super(PrinterStatus, self).__init__(obj, style, name, display_name)
		self.settings = settings

""" liste des elements printables """

from functools import lru_cache

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

def check_previous(convert_func=None):
	def _check_previous(func):
		def wrapper(self, n_col_max):
			raw_val = getattr(self.obj, self.var_name)
			val = convert_func(raw_val) if convert_func else raw_val
			if self.prev != val:
				self.prev_str = func(self, val, n_col_max)
				return self.prev_str
			else:
				return  ['\033[{}C'.format(n_col_max)]
		return wrapper
	return _check_previous

class PrinterElement:
	""" class abstraite pour tous les element printable """
	def __init__(self, obj, param, style, name, display_name=None):
		self.obj = obj
		self.var_name = name
		self.param = param
		self.name = display_name if display_name is not None else name
		self.style_changed = True
		self.style = style

	#@lru_cache(maxsize=256)
	def _format(self, string, value, n_col):
		formatting_values = []
		style = self.style
		if 'color' in style:
			formatting_values.append(FOREGROUND_COLORS[style['color']])
		# if 'background' in style:
		# 	formatting_values.append(BACKGROUND_COLORS[style['background']])
		if value and 'letters' in style:
			value = style['letters'](value)
		if 'underline' in style:
			formatting_values.append('4')
		if 'light' in style:
			formatting_values.append('1')

		styled_string = ''.join(['\033[', ';'.join(formatting_values), 'm', '{}', '\033[0m'])
		base_string = string.format(value)
		unpadded_string = string.format(styled_string.format(value))
		padded_string = '{:{pos}{size}.{size}}'.format(base_string, pos=style['pos'], size=n_col)
		return padded_string.replace(base_string, unpadded_string)

	def to_string(self, n_col_max):
		""" retourne la string de l'element """
		raise NotImplementedError("needs to be overridden")

	def change_style(self, new_style):
		""" change le style de l'element """
		self.style_changed = True
		self.style = new_style

class PrinterConstant(PrinterElement):
	""" une string constante """
	def to_string(self, n_col_max):
		yield self._format('{}', self.var_name, n_col_max)

class PrinterTitle(PrinterElement):
	""" le titre d'une section """
	def to_string(self, n_col_max):
		val = str(getattr(self.obj, self.var_name))
		yield self._format('{}', val, n_col_max)

class PrinterBool(PrinterElement):
	""" un booleen, represente par une case a cocher """
	def to_string(self, n_col_max):
		res = '■' if bool(getattr(self.obj, self.var_name)) else ' '
		trunc_name = self.name
		if len(self.name) + 3 > n_col_max:
			trunc_name = '{}..'.format(self.name[:n_col_max - 5])
		yield self._format(trunc_name + '[{}]', res, n_col_max)

class PrinterNumeric(PrinterElement):
	""" une unite, similaire a int mais affiche param a la fin """
	def to_string(self, n_col_max):
		name = self.name
		val = str(getattr(self.obj, self.var_name))
		self_len = len(name) + len(val) + 1 + len(self.param)
		equal = '{:^{size}}'.format('=', size=between(1, n_col_max - self_len + 1, 3))
		res = '{}{}'.format(name, equal)
		if self_len > n_col_max:
			val = '{}..'.format(val[:n_col_max - 4 - len(self.param)])
		yield self._format(res + '{}', val + self.param, n_col_max)

class PrinterStr(PrinterElement):
	""" une string """
	def to_string(self, n_col_max):
		string = str(getattr(self.obj, self.var_name))
		string_len = len(string)
		name_len = len(self.name)
		if string_len + name_len + 4 > n_col_max:
			yield self._format('-{}:'.format(self.name), None, n_col_max)
			if string_len + 2 <= n_col_max:
				yield self._format('\'{}\'', string, string_len + 2)
			else:
				yield self._format('\'{}', string[:n_col_max - 2], n_col_max)
				i = n_col_max-2
				while i + n_col_max - 2 < string_len:
					yield self._format(' {} ', string[i:i+n_col_max-2], n_col_max)
					i += n_col_max - 1
				yield self._format(' {}\'', string[i:string_len], n_col_max)
		else:
			yield self._format('-{}:\'{}\''.format(self.name, '{}'), string, n_col_max)

	def __len__(self):
		value = getattr(self.obj, self.var_name)
		return len(self.name) + len(str(value)) + 1

class PrinterSep(PrinterElement):
	""" une ligne de separation """
	def to_string(self, n_col_max):
		yield n_col_max*self.param

class PrinterBar(PrinterElement):
	""" une bar de progression (val doit etre entre 0 et 1) """
	def to_string(self, n_col_max):
		val = between(0, getattr(self.obj, self.var_name), 1)
		name = self.name
		total = (n_col_max - len(name) - 3)
		progress = round(val*total)
		left = total - progress
		string = '{}{}'.format(name, ':[{}]')
		val = '{}{}'.format(progress*'■', left*' ')
		yield self._format(string, val, n_col_max)

class PrinterRatio(PrinterElement):
	def to_string(self, n_col_max):
		name = self.name
		val, val_max = getattr(self.obj, self.var_name)
		str_length = 2 + len(name) + len(str(val)) + len(str(val_max))
		if name:
			if str_length > n_col_max:
				taille = len(name) - str_length - n_col_max - 2
				base = '{:.{taille}}..:{}/{}'.format(name, '{}', val_max, taille=taille)
				yield self._format(base, val, n_col_max)
			else:
				yield self._format('{}:{}/{}'.format(name, '{}', val_max), val, n_col_max)
		else:
			yield self._format('{}/{}'.format('{}', val_max), val, n_col_max)

class PrinterStatus(PrinterElement):
	def __init__(self, obj, style, name, display_name, settings):
		super(PrinterStatus, self).__init__(obj, style, name, display_name)
		self.settings = settings

class PrinterGraphe(PrinterElement):
	def to_string(self, n_col_max):
		h = int(self.param)
		values = getattr(self.obj, self.var_name)
		strings = [[] for i in range(h)]
		prev = 0
		for val in values[-n_col_max//2:]:
			for ligne in range(h):
				if ligne == prev:
					if ligne == val:
						strings[ligne].append('──')
					elif ligne > val:
						strings[ligne].append('┐ ')
					elif ligne < val:
						strings[ligne].append('┘ ')
				elif ligne > prev:
					if ligne == val:
						strings[ligne].append('┌─')
					elif ligne > val:
						strings[ligne].append('  ')
					elif ligne < val:
						strings[ligne].append('│ ')
				elif ligne < prev:
					if ligne == val:
						strings[ligne].append('└─')
					elif ligne > val:
						strings[ligne].append('│ ')
					elif ligne < val:
						strings[ligne].append('  ')
			prev = val
			print()
		return map(lambda l: self._format('{}', ''.join(l), n_col_max), reversed(strings))

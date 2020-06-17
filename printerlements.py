""" liste des elements printables """

class PrinterElement:
	""" class abstraite pour tous les element printable """
	def __init__(self, obj, param, style, name, display_name=None):
		self.obj = obj
		self.var_name = name
		self.param = param
		self.name = display_name if display_name is not None else name
		self.style = style

	def to_string(self, n_col_max):
		""" retourne la string de l'element """
		raise NotImplementedError("needs to be overridden")

	def get_value(self):
		""" retourne l'attribut si obj est un obj,
			l'element du dict ou l'element de la liste """
		if isinstance(self.obj, dict):
			return self.obj[self.var_name]
		if isinstance(self.obj, list):
			return self.obj[int(self.var_name)]
		return getattr(self.obj, self.var_name)

	def change_style(self, new_style):
		""" change le style de l'element """
		self.style = new_style

class PrinterSep(PrinterElement):
	""" une ligne de separation """
	def to_string(self, n_col_max):
		yield n_col_max*self.param

class PrinterConstant(PrinterElement):
	""" une string constante """
	def to_string(self, n_col_max):
		yield self.style('{}', self.var_name, n_col_max)

class PrinterTitle(PrinterElement):
	""" le titre d'une section """
	def to_string(self, n_col_max):
		val = str(self.get_value())
		yield self.style('{}', val, n_col_max)

class PrinterBool(PrinterElement):
	""" un booleen, represente par une case a cocher """
	def to_string(self, n_col_max):
		value = '■' if bool(self.get_value()) else ' '
		string = trunc_string(self.name, n_col_max - 3) + '[{}]'
		yield self.style(string, value, n_col_max)

class PrinterNumeric(PrinterElement):
	""" une unite, similaire a int mais affiche param a la fin """
	def to_string(self, n_col_max):
		unit = self.param
		val = str(self.get_value())

		len_equal = len(self.name) + len(val) + 1 + len(unit)
		equal = PrinterNumeric.__get_equal(n_col_max, len_equal)
		len_name = n_col_max - len(unit) - len(val) - len(equal)
		res = '{}{}'.format(trunc_string(self.name, len_name), equal)

		yield self.style(res + '{}', val + unit, n_col_max)

	@staticmethod
	def __get_equal(n_col_max, str_length):
		""" return la chaine de char contenant le egal avec ou sans espace autour """
		return '{:^{size}}'.format('=', size=between(1, n_col_max - str_length + 1, 3))

class PrinterRatio(PrinterElement):
	""" un ration, la valeur doit etre une liste [val, val_max] """
	def to_string(self, n_col_max):
		name = self.name
		val, val_max = self.get_value()
		if name:
			name = trunc_string(name, n_col_max - 2 - len(str(val)) - len(str(val_max)))
			yield self.style('{}:{}/{}'.format(name, '{}', val_max), val, n_col_max)
		else:
			yield self.style('{}/{}'.format('{}', val_max), val, n_col_max)

class PrinterBar(PrinterElement):
	""" une bar de progression """
	def to_string(self, n_col_max):
		len_progress = (n_col_max - len(self.name) - 2 - int(bool(self.name)))
		nb_char = round(between(0, self.get_value(), 1)*len_progress)
		progress_bar = '{:<{size}}'.format(nb_char*'■', size=len_progress)
		yield self.style(self.__get_empty_bar(n_col_max), progress_bar, n_col_max)

	def __get_empty_bar(self, n_col_max):
		string = '[{}]'
		if self.name:
			name = trunc_string(self.name, n_col_max//2)
			string = name + ':' + string
		return string

class PrinterStr(PrinterElement):
	""" une string """
	def to_string(self, n_col_max):
		string = str(self.get_value())
		string_len = len(string)
		name_len = len(self.name)
		if string_len + name_len + 1 > n_col_max:
			yield self.style('{}:'.format(self.name), None, n_col_max)
			if string_len + 2 <= n_col_max:
				yield self.style('{}', string, string_len)
			else:
				yield self.style('{}', string[:n_col_max - 1], n_col_max)
				i = n_col_max-2
				while i + n_col_max - 2 < string_len:
					yield self.style(' {} ', string[i:i+n_col_max-2], n_col_max)
					i += n_col_max - 1
				yield self.style(' {}', string[i:string_len], n_col_max)
		else:
			yield self.style('{}:{}'.format(self.name, '{}'), string, n_col_max)

	def __len__(self):
		value = self.get_value()
		return len(self.name) + len(str(value)) + 1

def trunc_string(string, size):
	""" tronque la stirng pour quelle fasse size """
	if len(string) < size:
		return string
	return '{}..'.format(string[:size - 2])

def between(lower_bound, value, upper_bound):
	""" retourne le max/min de value entre lower_bound et upper_bound """
	return max(lower_bound, min(value, upper_bound))

""" liste des elements printables """

class PrinterElement:
	""" class abstraite pour tous les element printable """
	def __init__(self, obj, param, style, name, display_name=None):
		self.obj = obj
		self.var_name = name
		self.param = param
		self.name = display_name if display_name is not None else name
		self.style = style
		self.style.element = self

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
		yield self.style('{}', trunc_string(self.var_name, n_col_max), n_col_max)

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
		res = f'{trunc_string(self.name, len_name)}{equal}'

		yield self.style(res + '{}', val + unit, n_col_max)

	@staticmethod
	def __get_equal(n_col_max, str_length):
		""" return la chaine de char contenant le egal avec ou sans espace autour """
		return '{:^{size}}'.format('=', size=between(1, n_col_max - str_length + 1, 3))

class PrinterRatio(PrinterElement):
	""" un ration, la valeur doit etre une liste [val, val_max] """
	def to_string(self, n_col_max):
		name = self.name
		val = self.get_value()
		val_max = self.param
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

class PrinterRow:
	""" une ligne d'elements """
	def __init__(self, elements, sep=''):
		self.elements = elements
		self.sep = sep

	def to_string(self, n_col_max):
		res = []
		each_len = n_col_max/len(self.elements)
		for i, elem in enumerate(self.elements):
			res.append(next(elem.to_string(round((i+1)*each_len)-round(i*each_len))))
		yield self.sep.join(res)

class PrinterInput(PrinterElement):
	""" un element avec lequel user peut interagir """
	def __init__(self, callback, style, name=None):
		self.callback = callback
		self.name = name if name else ''
		self.style = style
		self.style.element = self
		self.is_selected = False

	def handle_char(self, char):
		""" gere l'input user d'un character """
		raise NotImplementedError()

	def select(self):
		""" selectionne l'input """
		self.is_selected = True
		self.style.kwargs['underline'] = True

	def deselect(self):
		""" deselectionne l'input """
		self.is_selected = False
		self.style.kwargs['underline'] = False

class PrinterTextInput(PrinterInput):
	""" une input de text """
	def __init__(self, callback, style, name=None):
		super().__init__(callback, style, name)
		self.__content = []

	def to_string(self, n_col_max):
		name = trunc_string(self.name, n_col_max//2)
		size = n_col_max-len(name)-3+int(not bool(name))
		value = ''.join(self.__content[-size:] + [(size-len(self.__content[-size:]))*' '])
		if name:
			yield self.style('{}:[{}]'.format(name, '{}'), value, n_col_max)
		else:
			yield self.style('[{}]', value, n_col_max)

	def handle_char(self, char):
		if char == b'\r':
			if self.callback:
				self.callback(''.join(self.__content))
				self.clear()
		elif char == b'\x1b':
			self.clear()
		elif char == b'\x08':
			if self.__content:
				self.__content.pop()
		else:
			self.__content.append(char.decode('utf-8'))

	def get_value(self):
		return ''.join(self.__content)

	def clear(self):
		""" vide le contenu de l'input """
		self.__content.clear()

class PrinterOptionsInput(PrinterInput):
	""" une input depuis une liste d'options """
	def __init__(self, callback, options, style):
		super().__init__(callback, style)
		self.options = options

	def to_string(self, n_col_max):
		text = []
		for key, opt in self.options.items():
			text.append('{}: {}'.format(key, opt))
		i = 0
		while i < len(text):
			last_index = i
			current_length = -1
			while i < len(text) and current_length + len(text[i]) < n_col_max:
				current_length += len(text[i]) + 2
				i += 1
			yield self.style('{}', ', '.join(text[last_index:i]), n_col_max)

	def handle_char(self, char):
		ascii_char = char.decode('utf-8')
		if ascii_char in self.options:
			self.callback(ascii_char)

class PrinterBoolInput(PrinterInput, PrinterBool):
	""" une checkbox """
	def __init__(self, callback, style, name=None):
		super().__init__(callback, style, name)
		self.value = False

	def get_value(self):
		return self.value

	def handle_char(self, char):
		if char == b'\r':
			self.value = not self.value
			if self.callback:
				self.callback(self.value)

class PrinterButtonInput(PrinterInput):
	""" un bouton """
	def __init__(self, callback, option, style, name=None):
		super().__init__(callback, style, name)
		self.option = option

	def handle_char(self, char):
		if char == b'\r':
			self.callback(self.option)

	def to_string(self, n_col_max):
		if self.is_selected:
			yield self.style('[ {} ]', self.option, n_col_max)
		else:
			yield self.style('  {}  ', self.option, n_col_max)

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
	if len(string) <= size:
		return string
	return '{}..'.format(string[:size - 2])

def between(lower_bound, value, upper_bound):
	""" retourne le max/min de value entre lower_bound et upper_bound """
	return max(lower_bound, min(value, upper_bound))

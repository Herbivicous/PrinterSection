""" refonte des elements """

# pylint: disable=C0330
COLORS = [
	'black',
	'red',
	'green',
	'yellow',
	'blue',
	'magenta',
	'cyan',
	'white',
	'extended',
	'default'
]

SEP_CHARS = {
	'=': '═',
	'-': '─'
}

def parse_section(string, section, index):
	""" parse une string representatn une section """
	while index != len(string):
		char = string[index]
		index += 1
		if char == '{':
			index = parse_element(string, section, index)
		else:
			section.add_sep(SEP_CHARS[char] if char in SEP_CHARS else char)

def parse_element(string, section, index):
	""" parse un element """
	index, name = parse_var_name(string, index)
	index, display_type = parse_display_type(string, index)
	index, param = parse_display_param(string, index)
	index, style = parse_style(string, index)
	index, display_name = parse_display_name(string, index)
	section.add_arg(display_type, name, param, display_name, **style)
	return index

def parse_var_name(string, index):
	""" parse le nom de la variable a afficher """
	name = []
	while string[index] != ':':
		name.append(string[index])
		index += 1
	return index + 1, ''.join(name)

def parse_display_type(string, index):
	""" parse le type de la variable """
	return index+2, string[index+1]

def parse_display_param(string, index):
	""" parse le parametre du type d'affichage """
	param = []
	while string[index] not in ':}':
		param.append(string[index])
		index += 1
	return index, ''.join(param)

def parse_style(string, index):
	""" parse le style de l'element """
	style = {'pos': '<'}
	if string[index] == '}':
		return index, style
	index += 1
	if string[index] == ':':
		return index, style
	if string[index] in '<^>':
		style['pos'] = string[index]
		index += 1
	index, color = parse_color(string, index)
	if color:
		style['color'] = color.lower()
		style['letters'] = find_letters(color)
	while string[index] not in ':}':
		if string[index] == '_':
			style['underline'] = True
		elif string[index] == '*':
			style['light'] = True
		index += 1
	return index, style

def parse_color(string, index):
	""" parse une couleur """
	color = []
	while string[index].isalpha():
		color.append(string[index])
		index += 1
	color = ''.join(color)
	if color != '':
		if color.lower() not in COLORS:
			raise ValueError('{} is not a valid color'.format(color))
	return index, color

def find_letters(color):
	""" determine si color est uppercase, lowercase ou capitalized """
	if color.lower() == color:
		return  lambda string: str(string).lower()
	if color.upper() == color:
		return lambda string: str(string).upper()
	if color.capitalize() == color:
		return lambda string: str(string).capitalize()
	raise ValueError('{} isn\'t lower case, nor upper case nor capitalized'.format(color))

def parse_display_name(string, index):
	""" parse le nom de la variable a afficher """
	name = []
	if string[index] == '}':
		return index + 1, None
	index += 1
	while string[index] != '}':
		name.append(string[index])
		index += 1
	return index + 1, ''.join(name)

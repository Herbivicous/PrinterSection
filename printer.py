""" Class Section et Printer, gerant l'affichage en sections """

import os
from sys import stdout
from collections import OrderedDict
from random import random
import shutil
from threading import Thread
from time import sleep
from itertools import repeat, product, chain, cycle
import readchar

import printerlements as p_elem
from printerstyle import Style
from printerparser import parse_section, parse_style

# pylint: disable=C0330
class PrinterSection:
	""" Une section de printer """
	def __init__(self, obj):
		self.obj = obj
		self.elements = []
		self.inputs = []

	def get_line(self, n_col_max):
		""" yield une nouvelle ligne a afficher, affiche des ' ' si tous
		les elements ont ete affiches """
		for elem in self.elements:
			for str_elem in elem.to_string(n_col_max):
				yield str_elem
		while True:
			yield n_col_max*' '

	def __factory(self, code, param, *args):
		constructors = {
		    'c': p_elem.PrinterConstant,
			't': p_elem.PrinterTitle,
			's': p_elem.PrinterStr,
			'n': p_elem.PrinterNumeric,
			'b': p_elem.PrinterBool,
			'p': p_elem.PrinterBar,
			'r': p_elem.PrinterRatio,
			'ti': p_elem.PrinterTextInput,
			'oi': p_elem.PrinterOptionsInput,
			'bi': p_elem.PrinterBoolInput,
			'bu': p_elem.PrinterButtonInput,
		}
		return constructors[code](self.obj, param, *args)

	def __add_element(self, element):
		self.elements.append(element)
		return element

	def __add_ielement(self, element):
		self.inputs.append(element)
		return element

	def __add_arg(self, code, style, attr_name, display_name=None, param=None):
		""" ajoute un element a la section, de type 'code' """
		style_obj = Style(**style)
		new_printer_elem = self.__factory(code, param, style_obj, attr_name, display_name)
		style_obj.element = new_printer_elem
		self.elements.append(new_printer_elem)
		return new_printer_elem

	def __add_input(self, code, style, callback, display_name=None):
		style_obj = Style(**style)
		new_printer_elem = self.__factory(code, callback, style_obj, display_name)
		style_obj.element = new_printer_elem
		self.elements.append(new_printer_elem)
		self.inputs.append(new_printer_elem)
		return new_printer_elem

	def constant(self, value, **style):
		""" ajoute une constante a la section """
		return self.__add_arg('c', style, value, None, None)

	def title(self, attr_name, **style):
		""" ajoute un titre a la section """
		return self.__add_arg('t', style, attr_name, None, None)

	def string(self, attr_name, display_name, **style):
		""" ajoute une string a la section """
		return self.__add_arg('s', style, attr_name, display_name)

	def numeric(self, attr_name, display_name=None, unit='', **style):
		""" ajoute un nombre a la section """
		return self.__add_arg('n', style, attr_name, display_name, unit)

	def bool(self, attr_name, display_name=None, **style):
		""" ajoute un booleen a la section """
		return self.__add_arg('b', style, attr_name, display_name, None)

	def bools(self, attr_names, **style):
		elements = list(map(lambda name: p_elem.PrinterBoolInput(None, Style(**style), name), attr_names))
		row = p_elem.PrinterRow(elements)
		list(map(self.__add_ielement, elements))
		return self.__add_element(row)

	def progress(self, attr_name, display_name=None, **style):
		""" ajoute une bar de progression a la section """
		return self.__add_arg('p', style, attr_name, display_name, None)

	def ratio(self, attr_name, val_max, display_name=None, **style):
		""" ajoute un ratio a la section """
		return self.__add_arg('r', style, attr_name, display_name, val_max)

	def sep(self, char):
		""" ajoute une separation horizontale constituee de 'char' """
		better_char = {'=': '═', '-': '─'}.get(char, char)
		return self.__add_element(p_elem.PrinterSep(self.obj, better_char, Style(), None))

	def text_input(self, callback, name=None, **style):
		""" ajoute un champ texte """
		element = p_elem.PrinterTextInput(callback, Style(**style), name)
		return self.__add_element(self.__add_ielement(element))

	def options_input(self, callback, options, **style):
		""" ajoute une input de type options """
		element = p_elem.PrinterOptionsInput(callback, options, Style(**style))
		return self.__add_element(self.__add_ielement(element))

	def bool_input(self, callback, display_name=None, **style):
		""" ajoute une input de type bool """
		element = p_elem.PrinterBoolInput(callback, Style(**style), display_name)
		return self.__add_element(self.__add_ielement(element))

	def button(self, callback, text, **style):
		""" ajoute un bouton """
		element = p_elem.PrinterButtonInput(callback, text, Style(**style))
		return self.__add_element(self.__add_ielement(element))

	def inputs_iter(self):
		return iter(self.inputs)

def get_screen_size():
	""" return the size of the terminal """
	win_size = shutil.get_terminal_size(fallback=(80, 24))
	if win_size:
		width, height = win_size
	else:
		unix_size = os.popen('stty size', 'r').read().split()
		height, width = unix_size
	return (int(width), int(height))

class Printer:
	""" gestion d'un printer, compose de plusieurs sections """
	def __init__(self, cols, rows, **kwargs):
		self.sections = {}
		self.added_section = 0
		self.structure = (cols, rows)
		self.size = get_screen_size()
		self._set_args(kwargs)
		self.available_coords = list(product(range(rows), range(cols)))

	def __get_available_coords(self):
		if self.available_coords:
			pos_y, pos_x = self.available_coords.pop(0)
			return (pos_x, pos_y)
		raise StopIteration()

	def _set_args(self, kwargs):
		""" set les valeurs en fonction des arguments passes par kwargs """
		self.clear = kwargs.get('clear_terminal', True)

	def add_section(self, obj=None, *, x=None, y=None):
		""" ajoute une section au coordonnees si donnees, sinon a une case libre """
		new_section = PrinterSection(obj)
		if x is None or y is None:
			(x, y) = self.__get_available_coords()
		else:
			if (x, y) in self.available_coords:
				self.available_coords.remove((x, y))
		self.sections[(x, y)] = new_section
		return new_section

	def main_loop(self):
		inputs_iter = self.__inputs_iter()
		current = next(inputs_iter)
		current.select()
		while True:
			char = readchar.readchar()
			if char == b'\t':
				current.deselect()
				current = next(inputs_iter)
				current.select()
			else:
				current.handle_char(char)

	def __inputs_iter(self):
		return cycle(chain(*[section.inputs_iter() for section in self.sections.values()]))

	def __getitem__(self, key):
		return self.sections[key]

	def print(self):
		""" actualise la vue """
		if self.clear:
			# stdout.write("\033[?25l")
			stdout.write("\033[0;0H")
		width, height = self.size
		n_sec_per_line, n_sec_per_col = self.structure
		n_l = height // n_sec_per_col - 1
		n_c = width // n_sec_per_line - 1
		sections_line_string = []
		for i_sec_line, sec_line in enumerate(range(n_sec_per_col)):
			sections_line_string.append(Printer._get_top_border(n_c, i_sec_line, n_sec_per_line))
			line_iters = self._build_line_iters(n_sec_per_line, sec_line, n_c)
			sections_line_string.append(Printer._get_all_section_lines(line_iters, n_l))
		stdout.write('\n'.join(sections_line_string))
		stdout.flush()

	def _build_line_iters(self, n_sec_per_line, sec_line, n_col_max):
		""" retourne une liste d'iterateurs sur les lignes d'une section """
		line_iterators = []
		for sec_col in range(n_sec_per_line):
			coord = (sec_col, sec_line)
			if coord in self.sections:
				section = self.sections[coord]
				line_iterators.append(section.get_line(n_col_max))
			else:
				line_iterators.append(repeat(' '*n_col_max))
		return line_iterators

	@staticmethod
	def _get_all_section_lines(line_iters, n_l):
		""" ecrit dans stdout toutes les lignes de txt venant des lineiters """
		lines = []
		for i, col_line in enumerate(zip(*line_iters)):
			line = ['{}║'.format(str_line) for str_line in col_line]
			lines.append(''.join(line))
			if i >= n_l - 1:
				break
		return '\n'.join(lines)

	@staticmethod
	def _get_top_border(n_c, i_sec_line, n_sec_per_line):
		cross_char = '╬' if i_sec_line else '╦'
		last_cross_char = '╣' if i_sec_line else '╗'
		top_border = '{:═>{size}}'.format(cross_char, size=n_c+1)
		last_top_border = '{:═>{size}}'.format(last_cross_char, size=n_c+1)
		return '{}{}'.format((n_sec_per_line-1)*top_border, last_top_border)

	@staticmethod
	def restore():
		""" restaure l'affichage de l'invite de commande, marche pas trop """
		stdout.write('\033[?25h')
		stdout.flush()

def auto_print(printer, sleep_time, callback=None):
	""" print en chaine le printer """
	def refresh():
		while True:
			if callback:
				callback()
			printer.print()
			sleep(sleep_time)
	thread = Thread(target=refresh, daemon=True)
	thread.start()
	return thread

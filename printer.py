""" Class Section et Printer, gerant l'affichage en sections """

import os
from sys import stdout
from collections import OrderedDict
from random import random
import shutil
from threading import Thread
from time import sleep
from math import sqrt

import printerlements as p_elem
from printerparser import parse_section, parse_style

# pylint: disable=C0330
class PrinterSection:
	""" Une section de printer """
	def __init__(self, obj):
		self.obj = obj
		self.elements = OrderedDict()

	def get_line(self, n_col_max):
		""" yield une nouvelle ligne a afficher, affiche des ' ' si tous
		les elements ont ete affiches """
		for elem in self.elements.values():
			for str_elem in elem.to_string(n_col_max):
				yield str_elem
		while True:
			yield n_col_max*' '

	def __factory(self, code, attr_name, param, style, display_name):
		constructors = {
			't': p_elem.PrinterTitle,
			's': p_elem.PrinterStr,
			'n': p_elem.PrinterNumeric,
			'b': p_elem.PrinterBool,
			'p': p_elem.PrinterBar,
			'r': p_elem.PrinterRatio,
			'g': p_elem.PrinterGraphe,
		}
		return constructors[code](self.obj, param, style, attr_name, display_name)

	def add_arg(self, code, attr_name, param, style, display_name=None):
		""" ajoute un element a la section, de type 'code' """
		new_printer_elem = self.__factory(code, attr_name, param, style, display_name)
		self.elements[attr_name] = new_printer_elem

	def add_sep(self, char):
		""" ajoute une separation horizontale constituee de 'char' """
		self.elements[random_id()] = p_elem.PrinterSep(self.obj, char, {}, None)

	def change_style(self, var_name, style):
		""" change le style de var_name en style """
		new_style = parse_style(style, 0)[1]
		self.elements[var_name].style = new_style

	def get_printable(self, attr_name):
		if attr_name not in self.elements:
			raise AttributeError('{} doesn\'t exists'.format(attr_name))
		return self.elements[attr_name]

def random_id():
	""" retourne une id aleatoire """
	return str(round(10000*random()))

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
	def __init__(self, **kwargs):
		self.sections = []
		self.structure = None
		self.size = get_screen_size()
		self._set_args(kwargs)

	def _set_args(self, kwargs):
		""" set les valeurs en fonction des arguments passes par kwargs """
		self.refresh = kwargs.get('refresh_structure', True)
		self.clear = kwargs.get('clear_terminal', True)

	def find_structure_old(self):
		""" trouve la disposition de section se rapprochant le plus de 3/2 """
		target = 0.208*len(self.sections) + 1.79
		ratio_list = []
		for i in range(1, len(self.sections)+1):
			if (len(self.sections)/i).is_integer():
				ratio_list.append((int(len(self.sections)/i), i))
		best_ratio = min(ratio_list, key=lambda n: abs(n[0] - target))
		self.structure = best_ratio
		if best_ratio[0] == 1:
			self.sections.append(PrinterSection(None))
			self.find_structure()

	def find_structure(self):
		""" trouve la disposition de section se rapprochant le plus de 3/2 """
		n_section = len(self.sections)
		columns = [0, 1, 2, 3, 2, 3, 3, 4, 4, 3, 5, 4, 4, 5, 5, 5, 4, 6, 6, 5, 5, 7, 6]
		add = [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 2, 1, 0, 0, 1, 0, 1, 0, 0, 2]
		for _ in range(add[n_section]):
			self.sections.append(PrinterSection(None))
		self.structure = (columns[n_section], int(len(self.sections)/columns[n_section]))

	def add_section(self, format_obj, obj):
		""" ajoute une nouvelle section, en parsant format string """
		format_string = ''.join(format_obj) if isinstance(format_obj, list) else format_obj
		new_section = PrinterSection(obj)
		parse_section(format_string, new_section, 0)
		self.sections.append(new_section)
		return new_section

	def __getitem__(self, key):
		return self.sections[key]

	def print(self):
		""" actualise la vue """
		if self.clear:
			# stdout.write("\033[?25l")
			stdout.write("\033[0;0H")
		if self.refresh:
			self.find_structure()
		width, height = self.size
		n_sec_per_line = self.structure[0]
		n_sec_per_col = self.structure[1]
		n_l = height // n_sec_per_col - 1
		n_c = width // n_sec_per_line - 1
		sections_line_string = []
		for i_sec_line, sec_line in enumerate(range(n_sec_per_col)):
			sections_line_string.append(Printer._get_top_border(n_c, i_sec_line, n_sec_per_line))
			line_iters = self._build_line_iters(n_sec_per_line, sec_line, n_c)
			sections_line_string.append(Printer._get_all_section_lines(line_iters, n_l, n_c, width))
		stdout.write('\n'.join(sections_line_string))
		stdout.flush()

	def _build_line_iters(self, n_sec_per_line, sec_line, n_col_max):
		""" retourne une liste d'iterateurs sur les lignes d'une section """
		line_iterators = []
		for sec_col in range(n_sec_per_line):
			section = self.sections[n_sec_per_line * sec_line + sec_col]
			line_iterators.append(section.get_line(n_col_max))
		return line_iterators

	@staticmethod
	def _get_all_section_lines(line_iters, n_l, n_c, width):
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

def auto_print(printer, sleep_time):
	""" print en chaine le printer """
	def refresh():
		while True:
			printer.print()
			sleep(sleep_time)
	thread = Thread(target=refresh, daemon=True)
	thread.start()
	return thread

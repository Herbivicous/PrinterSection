""" test du printer en utilisant l'api weather """

#pylint: disable=all
from random import randint
import time

from urllib.request import urlopen
from urllib.error import HTTPError
from json import loads

from printer import Printer, auto_print

api_key = '2ad9512119b1c9aca49c6a9c14186dd0'
api_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

user_names = [
	'Jean',
	'Tonton',
	'Pipo',
	'Toto'
]

ME = 'Bastien'

def chat_section(main_printer, chatname):
	if chatname not in user_names:
		return
	chat = Chat(ME, chatname)
	section = main_printer.add_section(chat)
	section.title('name', align='center', strf='upper', underline=True, color='#123456')
	section.sep('-')
	# section.ratio('ratio', 10, 'Test')
	# section.title('weather', pos='^', light=True, color='cyan')
	# section.title('descr', pos='^')
	# section.sep(' ')
	# section.numeric('temp', 'Temperature', '°C', colorf=lambda t: 'red' if t>15 else 'blue')
	# section.numeric('humidity', 'Humidity', '%', color='green')
	# section.sep(' ')
	# section.progress('day_pr', 'Day', color='green')
	# section.bool('nuit', 'Night', pos='^', color='red')
	section.bool('online', 'Online', color='green', align='center')
	section.bool_input(lambda v: v, 'Mute', color='red', align='center')
	section.text_input(chat.add_me_msg, 'msg')
	# section.bool('valide', 'Selection', pos='<', color='green')
	chat.set_section(section)

class Chat:
	def __init__(self, me, name):
		self.section = None
		self.me = me
		self.name = name
		self.online = bool(randint(0, 1))

	def set_section(self, section):
		self.section = section

	def add_me_msg(self, msg):
		self.__add_msg(self.me, msg, 'green')
		if self.online:
			self.add_other_msg(msg[::-1])
		else:
			self.__add_msg('Error', '{} is offline'.format(self.name), 'red')

	def add_other_msg(self, msg):
		self.__add_msg(self.name, msg, 'cyan')

	def __add_msg(self, user, msg, color):
		if msg:
			self.section.constant('{}:{}'.format(user, msg), color=color)

main_printer = Printer(4, 3)

options = {'a': 'Abruti', 'q': 'Quit', 'p': 'peepee'}
f_quit = lambda v: v == 'q' and exit(0) or new_chat_section.constant(v, align='center')

new_chat_section = main_printer.add_section(None)
new_chat_section.options_input(f_quit, options, color='red')
new_chat_section.text_input(lambda v: chat_section(main_printer, v), 'Open chat with')

# N = 1000
# t0 = time.time()
# for _ in range(N):
# 	main_printer.print()
# t1 = time.time()
# print('\nfps = {}'.format(N/(t1 - t0)))

auto_print(main_printer, 0.1)
main_printer.main_loop()

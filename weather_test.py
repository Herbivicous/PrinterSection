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

city_names = [
	'Grenoble',
	'Paris',
	'Osaka',
	'Tokyo',
	'London',
	'Detroit',
	'Seattle',
	'LasVegas',
	'Sydney',
	'Calcutta',
	'Moscow',
	'Brasilia'
]

template = [
	'{name:%t:^BLUE_}',
	'{time:%t:^cyan}',
	'-',
	'{weather:%t:^cyan*}',
	'{descr:%t:^}',
	' ',
	'{temp:%n°C::Temperature}',
	'{humidity:%n%:green:Humidity}',
	' ',
	'{day_pr:%p:green:Day}',
	'{nuit:%b:^red:Night}'
]

class City:
	def __init__(self, name):
		self.name = name
		self.url = api_url.format(name, api_key)

	def update(self):
		# self.temp = randint(10, 1000)
		try:
			data = loads(urlopen(self.url).read())
		except HTTPError as error:
			print(self.url)
			raise error
		self.temp = round(data['main']['temp'] - 273.15, 2)
		style = '{BLUE}' if self.temp < 18 else '{RED}'
		self.section.change_style('temp', style)
		d_start = data['sys']['sunrise']
		d_end = data['sys']['sunset']
		now = int(time.time())
		self.nuit = now < d_start or now > d_end
		self.weather = '[ {} ]'.format(data['weather'][0]['main'])
		self.descr = data['weather'][0]['description']
		day_pr = (now - d_start)/(d_end - d_start)
		self.day_pr = day_pr if day_pr < 1 else 0
		self.humidity = data['main']['humidity']
		self.time = time.strftime('%H:%M', time.localtime(now - 7200 + data['timezone']))

cities = [City(name) for name in city_names]
main_printer = Printer()
for city in cities:
	city.section = main_printer.add_section(template, city)

for city in cities:
	city.update()

N = 1000
t0 = time.time()
for _ in range(N):
	main_printer.print()
t1 = time.time()
print('\ntime per frame = {}'.format((t1 - t0)/N))
print('fps = {}'.format(N/(t1 - t0)))

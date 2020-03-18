""" test de la lib de printer """

from sys import argv
from time import sleep
from random import randint
from printer import Printer, auto_print

def between(lower_bound, value, upper_bound):
	""" retourne le max/min de value entre lower_bound et upper_bound """
	return max(lower_bound, min(value, upper_bound))


class A:
	def __init__(self):
		self.titre = 'tit'
		self.a = 581634581634581
		self.b = 'toto'
		self.c = True
		self.bar = 0.514641
		self.rat = (5, 10)
		self.tab = [randint(0, 9)]
		for i in range(15):
			self.tab.append(between(0, self.tab[-1] + randint(-1, 1), 9))

	def add_value(self):
		self.tab.append(between(0, self.tab[-1] + randint(-1, 1), 9))

def main():
	""" tests """
	p = Printer()
	# p.add_section('{titre:%t:red}={a:%i:yellow}{b:%s:_:toto}{c:%b}{bar:%p:green}', s)
	# p.add_section('{titre:%t:blue}={a:%i:yellow}{b:%s:_:toto}{c:%b}{bar:%p:green}', s)
	# p.add_section('{titre:%t:red}-{b:%s:_:toto}{c:%b}{bar:%p:green}', s)
	# p.add_section('{titre:%t:blue}={a:%i:yellow}{b:%s:_:toto}{c:%b}{bar:%p:green}', s)
	# p.add_section('{titre:%t:red}={a:%i:yellow}{b:%s:_:toto}{c:%b}{bar:%p:green}', s)
	# p.add_section('{titre:%t:blue}={a:%i:yellow}{b:%s:_:toto}{c:%b}{bar:%p:green}', s)
	# p.add_section('{titre:%t:red}={a:%i:yellow}{b:%s:_:toto}{c:%b}{bar:%p:green}', s)
	# p.add_section('{titre:%t:blue}={a:%i:yellow}{b:%s:_:toto}{c:%b}{bar:%p:green}', s)
	# p.add_section('{titre:%t:red}-{b:%s:_:toto}{c:%b}{bar:%p:green}', s)
	# p.add_section('{titre:%t:blue}={a:%i:yellow}{b:%s:_:toto}{c:%b}{bar:%p:green}', s)
	# p.add_section('{titre:%t:red}={a:%i:yellow}{b:%s:_:toto}{c:%b}{bar:%p:green}', s)
	# p.add_section('{titre:%t:blue}={a:%i:yellow}{b:%s:_:toto}{c:%b}{bar:%p:green}', s)
	# p.add_section('{titre:%t:red}-{b:%s:_:toto}{c:%b}{bar:%p:green}', s)
	secs = [A() for _ in range(int(argv[1]))]
	p.sections = []	
	for sec in secs:
		p.add_section('{titre:%t:>red_}-{tab:%g10}-', sec)
	auto_print(p, 0.5)

	# for _ in range(int(argv[1])):
	# 	p.add_section('{titre:%t:blue}={a:%i:yellow:mort}{b:%s:_:toto}{c:%b}{bar:%p:green}', s)
	# p[0].change_style('a', '{white_}')
	# p.print()
	# auto_print(p, 1)
	# sleep(10)

	#print(len('\033[1;2;3'))
	for i in range(10):
		for sec in secs:
			sec.add_value()
		sleep(1)


if __name__ == '__main__':
	main()

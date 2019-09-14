""" test de la lib de printer """

from sys import argv
from time import sleep
from printer import Printer, auto_print


class A:
	pass

def main():
	""" tests """
	p = Printer()
	s = A()
	s.titre = 'tit'
	s.a = 581634581634581
	s.b = 'toto'
	s.c = True
	s.bar = 0.514641
	s.rat = (5, 10)
	s.tab = [0, 1, 2, 1, 2, 0, 1, 1, 1, 1, 0, 2, 1]
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
	p.sections = []	
	for i in range(1, int(argv[1])+1):
		p.add_section('{titre:%t:>red_}{tab:%g3}', s)
	p.print()

	# for _ in range(int(argv[1])):
	# 	p.add_section('{titre:%t:blue}={a:%i:yellow:mort}{b:%s:_:toto}{c:%b}{bar:%p:green}', s)
	# p[0].change_style('a', '{white_}')
	# p.print()
	# auto_print(p, 1)
	# sleep(10)

	print(len('\033[1;2;3'))


if __name__ == '__main__':
	main()

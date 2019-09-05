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
	s.a = 581634
	s.b = 'toto'
	s.c = False
	s.bar = 0.514641
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
	# for i in range(1, int(argv[1])+1):
	# 	p.sections = []
	# 	for j in range(i):
	# 		p.add_section('{titre:%t:blue}={a:%i::mort}{b:%s:_:toto}{c:%b}{bar:%p:green}', s)
	# 	p.print()
	# 	sleep(1)

	# for _ in range(int(argv[1])):
	# 	p.add_section('{titre:%t:blue}={a:%i:yellow:mort}{b:%s:_:toto}{c:%b}{bar:%p:green}', s)
	# p[0].change_style('a', '{white_}')
	# p.print()
	# auto_print(p, 1)
	# sleep(10)

	print(len('\033[1;2;3'))


if __name__ == '__main__':
	main()

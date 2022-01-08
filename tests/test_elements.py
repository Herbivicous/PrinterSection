
# from unittest import TestCase

# from src.sections.Element import PrinterSep, PrinterText, PrinterTitle

# class ElementTestCase:

# 	def __init__(self):
# 		self.element = None

# 	# def test_long_span(self):
# 	# 	""" tests that the span of every line is equal to the right value """

# 	# 	span = 20

# 	# 	for line in self.element.iter_lines(span):
# 	# 		print(line)
# 	# 		assert len(line.template) + len(line.value) == span

# 	# def test_short_span(self):
# 	# 	""" tests that the span of every line is equal to the right value """

# 	# 	span = 5

# 	# 	for template, value in self.element.lines(span):
# 	# 		assert len(template) + len(value) == span

# class TestPrinterSep(TestCase, ElementTestCase):

# 	def setUp(self):
# 		self.element = PrinterSep('@')

# 	def test_all_same_char(self):
# 		lines = list(self.element.lines(10))
# 		assert len(lines) == 1
# 		assert len(lines[0][0].replace('@', '')) == 0

# class TestPrinterText(TestCase, ElementTestCase):

# 	def setUp(self):
# 		self.element = PrinterText('bonjour toi')

# class TestPrinterTitle(TestCase, ElementTestCase):

# 	def setUp(self):
# 		self.element = PrinterTitle('bonjour toi')

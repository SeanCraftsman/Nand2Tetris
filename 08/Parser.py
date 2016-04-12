
class Parser(object):
	"""docstring for Parser"""
	def __init__(self, rfile):
		self.rfile = open(rfile,'r')
		self.advance()
		self.Arith = ('add','sub','neg','eq','gt','lt','and','or','not')

	def hasMoreCommands(self):
		if self.line:
			return True
		else:
			return False

	def advance(self):
		self.line = self.rfile.readline()
		while self.line.startswith('//') or \
			self.line == '\n':
			self.line = self.rfile.readline()
		self.text = self.line.split('//')[0]

	def commandType(self):
		if self.text.startswith('push'):
			return 'C_PUSH'
		elif self.text.startswith('pop'):
			return 'C_POP'
		elif self.text.strip() in self.Arith:
			return 'C_ARITHMETIC'
		elif self.text.startswith('label'):
			return 'C_LABEL'
		elif self.text.startswith('if-goto'):
			return 'C_IF'
		elif self.text.startswith('goto'):
			return 'C_GOTO'
		elif self.text.startswith('function'):
			return 'C_FUNCTION'
		elif self.text.startswith('return'):
			return 'C_RETURN'
		elif self.text.startswith('call'):
			return 'C_CALL'
	
	def arg1(self):
		if self.commandType() is 'C_ARITHMETIC':
			return self.text.strip()
		else:
			lst = self.text.split(' ')
			return lst[1]

	def arg2(self):
		if self.commandType() in ('C_POP','C_PUSH','C_FUNCTION','C_CALL'):
			lst = self.text.split(' ')
			return lst[2]
		else:
			print '--Error, No arg2!--'
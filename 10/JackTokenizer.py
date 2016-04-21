class Tokenizer(object):
	"""docstring for Tokenizer"""
	def __init__(self, rfilename):
		self.token = ''
		self.SymbleTable=('{','}','(',')','[',']','.',',',\
			';','+','-','*','/','&','|','<','>','=','~')
		self.KeyWordtable=('class','constructor','function',\
			'method','field','static','var','int','char','boolean',\
			'void','true','false','null','this','let','do','if',\
			'else','while','return')

		# clear comments
		readfile = open(rfilename,'r')
		copyfile = open('copyfile','w')
		while line=readfile.readline():
			while line == '\n' or line.startswith('//'):
				line=readfile.readline()
			if '//' in line:
				line=line[:line.find('//')]
			if '/*' in line:
				aline=line[:line.find('/*')]
				while line.find('*/')<0:
					line=readfile.readline()
				bline=line[line.find('*/')+2:]
				line=aline+bline
			copyfile.write(line)
		copyfile.close()
		readfile.close()
		self.rfile = open('copyfile','r')

	def hasMoreTokens(self):
		temp = self.rfile.read(1)
		while temp in '\n\t' and temp != '':
			temp = self.rfile.read(1)
		if not temp:
			return False
		else:
			self.rfile.seek(-1,1)
			return True

	def advance(self):
		self.token=''
		temp=self.rfile.read(1)

		if temp.isalpha() or temp.isdigit() or temp == '_':
			while temp.isalpha() or temp.isdigit() or temp == '_':
				self.token+=temp
				temp=self.rfile.read(1)
			if temp in self.SymbleTable or temp =='"':
				self.rfile.seek(-1,1)
			elif temp == ' ' or temp == '\n':
				self.rfile.seek(-1,1)
		elif temp in self.SymbleTable:
			self.token=temp
		elif temp =='"':
			self.token += '"'
			temp=self.rfile.read(1)
			while temp != '"':
				self.token+=temp
				temp=self.rfile.read(1)
			self.token+='"'

	def tokenType(self):
		if self.token in self.KeyWordtable:
			return 'KEYWORD'
		elif self.token in self.SymbleTable:
			return 'SYMBOL'
		elif self.token.isdigit():
			return 'INT_CONSTANT'
		elif self.token.startswith('"'):
			return 'STRING_CONSTANT'
		else:
			return 'IDENTIFIER'

	def Keyword(self):
		return self.token

	def Symbol(self):
		return self.token

	def Identifier(self):
		return self.token

	def intVal(self):
		return int(self.token)

	def stringVal(self):
		return self.token

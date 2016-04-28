#!/usr/bin/python

class Tokenizer():
	def __init__(self,rfile):
		copyfile = open('copyfile','w')
		line = rfile.readline()
		while line:
			while line == '\n' or line.startswith('//'):
				line=rfile.readline()
			if '//' in line:
				line=line[:line.find('//')]
			if '/*' in line:
				aline=line[:line.find('/*')]
				while line.find('*/')<0:
					line=readfile.readline()
				bline=line[line.find('*/')+2:]
				line=aline+bline
			copyfile.write(line)
			line = rfile.readline()
		copyfile.close()
		rfile.close()

		self.token = ''
		self.rfile = open('copyfile','r')
		self.STable=('{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~')
		self.KWtable=('class','constructor','function','method','field','static','var','int','char','boolean',\
		'void','true','false','null','this','let','do','if','else','while','return')


	def hasMoreTokens(self):
		temp=self.rfile.read(1)
		while temp in ' \n\t' and temp != '':
			temp=self.rfile.read(1)
		if not temp:
			return False
		else:
			self.rfile.seek(-1,1) # go back
			return True

	def advance(self):
		self.token=''
		temp=self.rfile.read(1)

		if temp.isalpha() or temp.isdigit() or temp == '_':
			while temp.isalpha() or temp.isdigit() or temp == '_':
				self.token+=temp
				temp=self.rfile.read(1)
			if temp in self.STable or temp =='"': # go back when the next is useful
				self.rfile.seek(-1,1)
			elif temp == ' ' or temp == '\n':
				self.rfile.seek(-1,1)

		elif temp in self.STable:
			self.token=temp
		elif temp =='"':
			self.token += '"'
			temp=self.rfile.read(1)
			while temp != '"':
				self.token+=temp
				temp=self.rfile.read(1)
			self.token+='"'

	def tokenType(self):
		if self.token in self.KWtable:
			return 'KEYWORD'
		elif self.token in self.STable:
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
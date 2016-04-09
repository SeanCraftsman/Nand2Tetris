
import sys,os

class Parser(object):
	"""docstring for Parser"""
	def __init__(self, rfile):
		self.rfile = rfile
		self.line = self.rfile.readline()
		self.text = self.line.split('//')[0]

	def hasMoreCommands(self):
		if self.line:
			return True
		else:
			return False

	def advance(self):
		self.line = self.rfile.readline()
		while self.line.startswith('//') or self.line == '\n':
			self.line = self.rfile.readline()
		self.text = self.line.split('//')[0]

	def commandType(self):
		if self.text.find('@')>=0:
			return 'A_COMMAND'
		elif self.text.find('=')>=0 or self.text.find(';')>=0:
			return 'C_COMMAND'
		elif self.text.find('(')>=0:
			return 'L_COMMAND'

	def symbol(self):
		symbol = self.text.strip(' @()\n')
		return symbol

	def dest(self):
		if self.text.find('=')>=0:
			destlist=self.text.split('=')
			return destlist[0].strip(' ')
		elif self.text.find(';')>=0:
			return 'None'
	def comp(self):
		if self.text.find('=')>=0:
			complist1=self.text.split('=')
			return complist1[1].strip('\n')
		elif self.text.find(';')>=0:
			complist2=self.text.split(';')
			return complist2[0].strip(' ')

	def jump(self):
		if self.text.find('=')>=0:
			return 'None'
		elif self.text.find(';')>=0:
			jumplist=self.text.split(';')
			return jumplist[1].strip(' \n')

class Code(object):
	"""docstring for Code"""
	def dest(self, destCode):
		d1 = d2 = d3 = '0'
		for item in destCode:
			if item == 'A':
				d1 = '1'
			elif item == 'D':
				d2 = '1'
			elif item == 'M':
				d3 = '1'
		return d1+d2+d3

	def comp(self, compCode):
		compDict = {
		'0'  :'101010',
		'1'  :'111111',
		'-1' :'111010',
		'D'  :'001100',
		'A'  :'110000',
		'!D' :'001101',
		'!A' :'110001',
		'-D' :'001101',
		'-A' :'110011',
		'D+1':'011111',
		'A+1':'110111',
		'D-1':'001110',
		'A-1':'110010',
		'D+A':'000010',
		'A+D':'000010',
		'D-A':'010011',
		'A-D':'000111',
		'D&A':'000000',
		'A&D':'000000',
		'D|A':'010101',
		'A|D':'010101'
		}
		if 'M' in compCode:
			a = '1'
			compCode = compCode.replace('M','A')
		else:
			a = '0'
		return a+compDict[compCode]

	def jump(self, jumpCode):
		jumpDict = {
		'None':'000',
		'JGT':'001',
		'JEQ':'010',
		'JGE':'011',
		'JLT':'100',
		'JNE':'101',
		'JLE':'110',
		'JMP':'111'
		}
		return jumpDict[jumpCode]

class SymbolTable(object):
	"""docstring for SymbolTable"""
	def __init__(self):
		self.labelDict = {
			'SP'  : '0',
			'LCL' : '1',
			'ARG' : '2',
			'THIS': '3',
			'THAT': '4',
			'SCREEN': '16384',
			'KBD': '24576',
			'R0' : '0',
			'R1' : '1',
			'R2' : '2',
			'R3' : '3',
			'R4' : '4',
			'R5' : '5',
			'R6' : '6',
			'R7' : '7',
			'R8' : '8',
			'R9' : '9',
			'R10' : '10',
			'R11' : '11',
			'R12' : '12',
			'R13' : '13',
			'R14' : '14',
			'R15' : '15',
		}
	def addEntry(self, symbol, addr):
		self.labelDict[symbol] = addr
	def contains(self, symbol):
		if symbol in self.labelDict.keys():
			return True
		else:
			return False
	def GetAddress(self, symbol):
		return self.labelDict[symbol]


def main():
	filename = sys.argv[1]
	rfile = open(filename, mode='r')
	wfile = open(filename.split('.')[0]+'.hack',mode='w')
	symbolTab = SymbolTable()
	parser = Parser(rfile)
	code = Code()
	i = 0
	#first loop
	while parser.hasMoreCommands():
		ctype = parser.commandType()
		if ctype == 'L_COMMAND':
			symbol = parser.symbol()
			symbolTab.addEntry(symbol,i-1)
		else:
			i += 1
		parser.advance()
	rfile.close()

	#second loop
	num = 16
	rfile = open(filename, mode='r')
	parser = Parser(rfile)
	while parser.hasMoreCommands():
		ctype = parser.commandType()
		if ctype == 'A_COMMAND':
			symbol = parser.symbol()
			if not symbol.isdigit():
				if symbolTab.contains(symbol):
					symbol = symbolTab.GetAddress(symbol)
				else:
					symbolTab.labelDict[symbol] = str(num)
					symbol = num
					num += 1
			ins = bin(int(symbol))
			ins = ins[2:]
			lenth = len(ins)
			if lenth <= 15:
				n = 16-lenth
				ins = n*'0'+ins
			else:
				print 'Error,ValueOverFlow!'
			wfile.write(ins+'\n')

		elif ctype == 'C_COMMAND':
			dest = parser.dest()
			comp = parser.comp()
			jump = parser.jump()
			ins = '111'+code.comp(comp)+code.dest(dest)+code.jump(jump)
			wfile.write(ins+'\n')

		parser.advance()

	rfile.close()
	wfile.close()

if __name__ == '__main__':
	main()

	
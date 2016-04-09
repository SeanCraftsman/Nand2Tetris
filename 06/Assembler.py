
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
			return None
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

def main():
	filename = sys.argv[1]
	rfile = open(filename, mode='r')
	wfile = open(filename.split('.')[0]+'.hack',mode='w')
	parser = Parser(rfile)
	code = Code()

	while parser.hasMoreCommands():
		ctype = parser.commandType()
		if ctype == 'A_COMMAND':
			print 'A:',parser.text,
			print '\t symbol:',parser.symbol()
		elif ctype == 'C_COMMAND':
			print 'C:',parser.text,
			print '\t dest:',parser.dest()
			print '\t comp:',parser.comp()
			print '\t jump:',parser.jump()
		elif ctype == 'L_COMMAND':
			print 'L:',parser.text,
			print '\t symbol:',parser.symbol()
		parser.advance()

	rfile.close()
	wfile.close()

if __name__ == '__main__':
	main()

	
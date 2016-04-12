
import sys,os
from Parser import Parser
from CodeWriter import CodeWriter

def Main(parser,codeWriter,filename):
    while parser.hasMoreCommands():
        ctype = parser.commandType()
        if ctype == 'C_ARITHMETIC':
            arg1 = parser.arg1().strip()
            codeWriter.writeArithmetic(arg1)
        elif ctype in ('C_PUSH','C_POP'):
            arg1 = parser.arg1().strip()
            arg2 = parser.arg2().strip()
            codeWriter.writePushPop(ctype,arg1,arg2,filename)
        elif ctype == 'C_LABEL':
            arg1 = parser.arg1().strip()
            codeWriter.writeLabel(arg1)
        elif ctype == 'C_GOTO':
            arg1 = parser.arg1().strip()
            codeWriter.writeGoto(arg1)
        elif ctype == 'C_IF':
            arg1 = parser.arg1().strip()
            codeWriter.writeIf(arg1)
        elif ctype == 'C_FUNCTION':
            arg1 = parser.arg1().strip()
            arg2 = parser.arg2().strip()
            codeWriter.writeFunction(arg1,arg2)
        elif ctype == 'C_RETURN':
            codeWriter.writeReturn()
        elif ctype == 'C_CALL':
            arg1 = parser.arg1().strip()
            arg2 = parser.arg2().strip()
            codeWriter.writeCall(arg1,arg2)
        parser.advance()
    parser.rfile.close()



filename = sys.argv[1]

if os.path.isfile(filename):
	parser = Parser(filename)
	codeWriter = CodeWriter()
	codeWriter.setFileName(filename)
	codeWriter.wfile.write('@256\nD=A\n@SP\nM=D\n')
	Main(parser,codeWriter,filename)
elif os.path.isfile('Sys.vm'):
	codeWriter = CodeWriter()
	codeWriter.setFileName(filename)
	codeWriter.wfile.write('@256\nD=A\n@SP\nM=D\n')
	codeWriter.wfile.write('@return_address0\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\
		\n@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\
		\n@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\
		\n@0\nD=A\n@5\nD=D+A\n@SP\nD=M-D\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\
		\n@Sys.init\n0;JMP\n(return_address0)\n')
	filelist = os.listdir(os.getcwd())
	for item in filelist:
		if item.endswith('.vm'):
			filename = item
			parser = Parser(filename)
			Main(parser,codeWriter,filename)
else:
	print '--Wrong Instruction!--'

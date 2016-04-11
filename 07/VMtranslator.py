
import sys,os
from Parser import Parser
from CodeWriter import CodeWriter

filename = sys.argv[1]
ps = Parser(filename)
cw = CodeWriter()
cw.setFileName(filename)
cw.wfile.write('@256\nD=A\n@SP\nM=D\n')

while ps.hasMoreCommands():
    ctype = ps.commandType()
    if ctype == 'C_ARITHMETIC':
        arg1 = ps.arg1().strip()
        cw.writeArithmetic(arg1)
    elif ctype in ('C_PUSH','C_POP'):
        arg1 = ps.arg1().strip()
        arg2 = ps.arg2().strip()
        cw.writePushPop(ctype,arg1,arg2)
    ps.advance()
    
ps.rfile.close()
cw.Close()

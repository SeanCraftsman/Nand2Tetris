
import sys,os
import Parser
import CodeWriter

filename = sys.argv[1]
rfile = open(filename,'r')
wfile = CodeWriter.setFileName(filename)
wfile.write('@256\nD=A\n@SP\nM=D\n')

line = Parser.advance(rfile)

while Parser.hasMoreCommands(line):
    while line == '\n' or line.startswith('//'):
        line = Parser.advance(rfile)
    ctype = Parser.commandType(line)
    if ctype == 'C_ARITHMETIC':
        arg1 = Parser.arg1(line).strip()
        CodeWriter.writeArithmetic(wfile,arg1)
    elif ctype in ('C_PUSH','C_POP'):
        arg1 = Parser.arg1(line).strip()
        arg2 = Parser.arg2(line).strip()
        CodeWriter.writePushPop(wfile,ctype,arg1,arg2)
    line = Parser.advance(rfile)
    
rfile.close()
CodeWriter.Close(wfile)


import sys,os
from Parser import Parser

class CodeWriter(object):
    """docstring for CodeWriter"""
    def __init__(self):
        self.count = 0

    def setFileName(self,filename):
        fileTuple = os.path.splitext(filename)
        self.wfile = open(fileTuple[0]+'.asm','w')

    def writeArithmetic(self,command):
        if command == 'add':
            self.wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D+M\n@SP\nM=M+1\n')
        elif command == 'sub':
            self.wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=M-D\n@SP\nM=M+1\n')
        elif command == 'neg':
            self.wfile.write('@SP\nM=M-1\nA=M\nM=-M\n@SP\nM=M+1\n')
        elif command == 'and':
            self.wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D&M\n@SP\nM=M+1\n')
        elif command == 'or':
            self.wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D|M\n@SP\nM=M+1\n')
        elif command == 'not':
            self.wfile.write('@SP\nM=M-1\nA=M\nM=!M\n@SP\nM=M+1\n')
        elif command == 'eq':
            self.wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=D-M\n@RET_TRUE'+str(self.count)+\
                        '\nD;JEQ\nD=0\n@CONTINUE'+str(self.count)+'\n0;JMP\n(RET_TRUE'+str(self.count)+')\n'\
                        +'D=-1\n(CONTINUE'+str(self.count)+')\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            self.count += 1
        elif command == 'gt':
            self.wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@RET_TRUE'+str(self.count)+\
                        '\nD;JGT\nD=0\n@CONTINUE'+str(self.count)+'\n0;JMP\n(RET_TRUE'+str(self.count)+')\n'\
                        +'D=-1\n(CONTINUE'+str(self.count)+')\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            self.count += 1
        elif command == 'lt':
            self.wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@RET_TRUE'+str(self.count)+\
                        '\nD;JLT\nD=0\n@CONTINUE'+str(self.count)+'\n0;JMP\n(RET_TRUE'+str(self.count)+')\n'\
                        +'D=-1\n(CONTINUE'+str(self.count)+')\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            self.count += 1
    def writePushPop(self,command, segment, index):
        if command == 'C_PUSH':
            if segment == 'constant':
                self.wfile.write('@'+index+'\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif segment == 'local':
                self.wfile.write('@LCL\nD=M\n@'+index+'\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif segment == 'argument':
                self.wfile.write('@ARG\nD=M\n@'+index+'\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif segment == 'this':
                self.wfile.write('@THIS\nD=M\n@'+index+'\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif segment == 'that':
                self.wfile.write('@THAT\nD=M\n@'+index+'\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif segment == 'pointer':
                if index == '0':
                    self.wfile.write('@THIS\n')
                elif index == '1':
                    self.wfile.write('@THAT\n')
                self.wfile.write('D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif segment == 'static':
                self.wfile.write('@'+index+'\nD=A\n@16\nD=A+D\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
            elif segment == 'temp':
                self.wfile.write('@'+index+'\nD=A\n@5\nD=A+D\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')    
                
        elif command == 'C_POP':
            if segment == 'local':
                self.wfile.write('@SP\nM=M-1\nA=M\nD=M\n@LCL\nA=M\n')
                for i in range(0,int(index)):
                    self.wfile.write('A=A+1\n')
                self.wfile.write('M=D\n')
            elif segment == 'argument':
                self.wfile.write('@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\n')
                for i in range(0,int(index)):
                    self.wfile.write('A=A+1\n')
                self.wfile.write('M=D\n')
            elif segment == 'this':
                self.wfile.write('@SP\nM=M-1\nA=M\nD=M\n@THIS\nA=M\n')
                for i in range(0,int(index)):
                    self.wfile.write('A=A+1\n')
                self.wfile.write('M=D\n')
            elif segment == 'that':
                self.wfile.write('@SP\nM=M-1\nA=M\nD=M\n@THAT\nA=M\n')
                for i in range(0,int(index)):
                    self.wfile.write('A=A+1\n')
                self.wfile.write('M=D\n')
            elif segment == 'pointer':
                self.wfile.write('@SP\nM=M-1\nA=M\nD=M\n')
                if index == '0':
                    self.wfile.write('@THIS\n')
                else:
                    self.wfile.write('@THAT\n')
                self.wfile.write('M=D\n')
            elif segment == 'static':
                self.wfile.write('@SP\nM=M-1\nA=M\nD=M\n@16\n')
                for i in range(0, int(index)):
                    self.wfile.write('A=A+1\n')
                self.wfile.write('M=D\n')
            elif segment == 'temp':
                self.wfile.write('@SP\nM=M-1\nA=M\nD=M\n@5\n')
                for i in range(0, int(index)):
                    self.wfile.write('A=A+1\n')
                self.wfile.write('M=D\n')
    def Close(self):
        self.wfile.close()


        







import sys,os
import Parser

CODEFLAG = 0


def setFileName(filename):
    fileTuple = os.path.splitext(filename)
    wfile = open(fileTuple[0]+'.asm','w')
    return wfile

def writeArithmetic(wfile, command):
    global CODEFLAG
    if command == 'add':
        wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D+M\n@SP\nM=M+1\n')
    elif command == 'sub':
        wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=M-D\n@SP\nM=M+1\n')
    elif command == 'neg':
        wfile.write('@SP\nM=M-1\nA=M\nM=-M\n@SP\nM=M+1\n')
    elif command == 'and':
        wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D&M\n@SP\nM=M+1\n')
    elif command == 'or':
        wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D|M\n@SP\nM=M+1\n')
    elif command == 'not':
        wfile.write('@SP\nM=M-1\nA=M\nM=!M\n@SP\nM=M+1\n')
    elif command == 'eq':
        wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=D-M\n@RET_TRUE'+str(CODEFLAG)+\
                    '\nD;JEQ\nD=0\n@CONTINUE'+str(CODEFLAG)+'\n0;JMP\n(RET_TRUE'+str(CODEFLAG)+')\n'\
                    +'D=-1\n(CONTINUE'+str(CODEFLAG)+')\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        CODEFLAG += 1
    elif command == 'gt':
        wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@RET_TRUE'+str(CODEFLAG)+\
                    '\nD;JGT\nD=0\n@CONTINUE'+str(CODEFLAG)+'\n0;JMP\n(RET_TRUE'+str(CODEFLAG)+')\n'\
                    +'D=-1\n(CONTINUE'+str(CODEFLAG)+')\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        CODEFLAG += 1
    elif command == 'lt':
        wfile.write('@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@RET_TRUE'+str(CODEFLAG)+\
                    '\nD;JLT\nD=0\n@CONTINUE'+str(CODEFLAG)+'\n0;JMP\n(RET_TRUE'+str(CODEFLAG)+')\n'\
                    +'D=-1\n(CONTINUE'+str(CODEFLAG)+')\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        CODEFLAG += 1

def writePushPop(wfile, command, segment, index):
    if command == 'C_PUSH':
        if segment == 'constant':
            wfile.write('@'+index+'\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        elif segment == 'local':
            wfile.write('@LCL\nD=M\n@'+index+'\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        elif segment == 'argument':
            wfile.write('@ARG\nD=M\n@'+index+'\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        elif segment == 'this':
            wfile.write('@THIS\nD=M\n@'+index+'\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        elif segment == 'that':
            wfile.write('@THAT\nD=M\n@'+index+'\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        elif segment == 'pointer':
            if index == '0':
                wfile.write('@THIS\n')
            elif index == '1':
                wfile.write('@THAT\n')
            wfile.write('D=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        elif segment == 'static':
            wfile.write('@'+index+'\nD=A\n@16\nD=A+D\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')
        elif segment == 'temp':
            wfile.write('@'+index+'\nD=A\n@5\nD=A+D\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n')    
            
    elif command == 'C_POP':
        if segment == 'local':
            wfile.write('@SP\nM=M-1\nA=M\nD=M\n@LCL\nA=M\n')
            for i in range(0,int(index)):
                wfile.write('A=A+1\n')
            wfile.write('M=D\n')
        elif segment == 'argument':
            wfile.write('@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\n')
            for i in range(0,int(index)):
                wfile.write('A=A+1\n')
            wfile.write('M=D\n')
        elif segment == 'this':
            wfile.write('@SP\nM=M-1\nA=M\nD=M\n@THIS\nA=M\n')
            for i in range(0,int(index)):
                wfile.write('A=A+1\n')
            wfile.write('M=D\n')
        elif segment == 'that':
            wfile.write('@SP\nM=M-1\nA=M\nD=M\n@THAT\nA=M\n')
            for i in range(0,int(index)):
                wfile.write('A=A+1\n')
            wfile.write('M=D\n')
        elif segment == 'pointer':
            wfile.write('@SP\nM=M-1\nA=M\nD=M\n')
            if index == '0':
                wfile.write('@THIS\n')
            else:
                wfile.write('@THAT\n')
            wfile.write('M=D\n')
        elif segment == 'static':
            wfile.write('@SP\nM=M-1\nA=M\nD=M\n@16\n')
            for i in range(0, int(index)):
                wfile.write('A=A+1\n')
            wfile.write('M=D\n')
        elif segment == 'temp':
            wfile.write('@SP\nM=M-1\nA=M\nD=M\n@5\n')
            for i in range(0, int(index)):
                wfile.write('A=A+1\n')
            wfile.write('M=D\n')
def Close(wfile):
    wfile.close()
        
        







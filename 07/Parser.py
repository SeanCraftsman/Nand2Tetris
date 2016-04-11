#!/usr/bin/python
Arith = ('add','sub','neg','eq','gt','lt','and','or','not')

def hasMoreCommands(line):
    # Return if there were more command in input
    if not line:
        return False
    else:
        return True

def advance(rfile):
    # Return the next command, should be called only if hasMoreCommands() is true
    line= rfile.readline()
    return line

def commandType(line):
    # Return the type of the current VM command
    if line.find('push')>= 0:
        return 'C_PUSH'
    elif line.find('pop')>=0:
        return 'C_POP'
    elif line.strip() in Arith:
        return 'C_ARITHMETIC'

def arg1(line):
    # Return the first argument of the command
    if commandType(line) is 'C_ARITHMETIC':
        return line.strip()
    else:
        spline = line.split(' ')
        return spline[1]

def  arg2(line):
    # Return the second argument of hte command
    
    if commandType(line) in ('C_POP','C_PUSH','C_FUNCTION','C_CALL'):
        spline=line.split(' ')
        return spline[2]

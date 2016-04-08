
filename = raw_input('Enter file name:')
asmname = filename + '.asm'
hackname = filename + '.hack'
asm = open(asmname, mode='r', buffering=-1)

CompCode = {
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
JumpCode = {
        'None':'000',
        'JGT':'001',
        'JEQ':'010',
        'JGE':'011',
        'JLT':'100',
        'JNE':'101',
        'JLE':'110',
        'JMP':'111'
        }

Label = {
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

def getText(x):
    text = x.readlines()
    count = 0
    for eachLine in text:
        eachLine = eachLine.replace('\n','')
        eachLine = eachLine.replace(' ','')
        text[count] = eachLine
        n = 0
        for item in eachLine:
            if item  == '/':
                text[count] = eachLine[:n]
                break
            elif item == ' ':
                text[count]
            n += 1
        count += 1
    while True:
        try:
            text.remove('')
        except:
            break

    return text

def handleLabel(text):
    newtext = []
    finaltext = []
    n = 16
    for eachLine in text:
        if eachLine[0] == '(':
            value = eachLine[1:-1]
            Label[value] = len(newtext)
        else:
            newtext.append(eachLine)
    for eachLine in newtext:
        if eachLine[0] == '@':
            value = eachLine[1:]
            try:
                value = int(value)
                finaltext.append(eachLine)
            except:
                if value in Label.keys():
                    finaltext.append('@'+ str(Label[value]))
                else:
                    Label[value] = str(n)
                    finaltext.append('@'+str(n))
                    n += 1
        else:
            finaltext.append(eachLine)
    return finaltext

def Ains(line):
    line = int(line[1:])
    ins = bin(line)
    ins = ins[2:]
    lenth = len(ins)
    if lenth <= 15:
        n = 15-lenth
        ins = (n+1)*'0'+ins
    else:
        print 'Error,ValueOverFlow!'
    return ins

def Cins(line):
    comp='D&A'
    dest=''
    jump='None'
    temp = line.split('=')
    if len(temp) == 2:
        dest = temp[0]
        line = temp[1]
    temp = line.split(';')
    if len(temp) == 2:
        comp = temp[0]
        jump = temp[1]
    else:
        comp = temp[0]

    if 'M' in comp:
        a = '1'
        comp = comp.replace('M','A')
    else:
        a = '0'
    
    cc = CompCode[comp]
    jj = JumpCode[jump]
    d1 = d2 = d3 = '0'
    for item in dest:
        if item == 'A':
            d1 = '1'
        elif item == 'D':
            d2 = '1'
        elif item == 'M':
            d3 = '1'
    dd = d1+d2+d3
    ins = '111'+ a + cc + dd +jj
    return ins

text = getText(asm)
text = handleLabel(text)
hack = open(hackname, mode='w', buffering=-1)
for eachLine in text:
    if eachLine[0] == '@':
        eachLine = Ains(eachLine)
    else:
        eachLine = Cins(eachLine)
    hack.write(eachLine+'\n')

asm.close()
hack.close()
a = raw_input('Finished!')


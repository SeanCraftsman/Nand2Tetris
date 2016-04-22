#!/usr/bin/python
import JackTokenizer
import CompilationEngine
import sys,os

filename=sys.argv[1]
readfile = open(filename,'r')

#clear all the // /* ... notes, create a new file to save the result
copyfile = open('copyfile','w')
line=readfile.readline()
while line:
	while line == '\n' or line.startswith('//'):
		line=readfile.readline()
	if '//' in line:
		line=line[:line.find('//')]
	if '/*' in line:
		aline=line[:line.find('/*')]
		while line.find('*/')<0:
			line=readfile.readline()
		bline=line[line.find('*/')+2:]
		line=aline+bline
	copyfile.write(line)
	line=readfile.readline()
copyfile.close()
readfile.close()

rfile=open('copyfile','r')
wfile=open(filename.strip('.jack')+'.xml','w')

outputCompile=CompilationEngine.Compile(rfile,wfile)
outputCompile.compileClass()

rfile.close()
wfile.close()
os.remove('copyfile')
Bline   详细X
网络释义
Bline: 变址寄存器
bline out: 贝尔出
bline film: 盲色片
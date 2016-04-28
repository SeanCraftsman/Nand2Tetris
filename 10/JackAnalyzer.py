#!/usr/bin/python

import JackTokenizer
import CompilationEngine
import sys,os

filename=sys.argv[1]
readFile = open(filename,'r')
writeFile = open(filename.split('.')[0]+'.xml','w')

tokenizer = JackTokenizer.Tokenizer(readFile)
compiler = CompilationEngine.Compile(tokenizer,writeFile)
compiler.compileClass()

readFile.close()
tokenizer.rfile.close()
writeFile.close()
os.remove("copyfile")


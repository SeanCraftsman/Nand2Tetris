#!/usr/bin/python
import JackTokenizer
import CompilationEngine
import sys,os

filename = sys.argv[1]
wfilename=filename.strip('.jack')+'.xml'
tokenizer = JackTokenizer.Tokenizer(filename)
outCompile = CompilationEngine.Compiler(tokenizer,wfilename)


os.remove('copyfile')
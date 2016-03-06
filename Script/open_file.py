#!/usr/bin/env python
import subprocess
def outfile():
	outputfile = open("test.txt","w")
	outputfile.write("hello, world !!!\nhello, word !!!")
	outputfile.close()
def manin():
	outfile()

manin()

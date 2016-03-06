#!/usr/bin/python
#
#========================================================================
# Author:Andre
# Email:yangjunfei2146@gmail.com
# File Name: 
# Description:
# Edit History:
# 2015-02-21 File created.
#========================================================================
import sys
import subprocess

def  shell_cmd(cmd):
	subprocess.PIPE
	#cmd= 'ping -c %s -i %s %s' % (3,0.01, "172.16.205."+str(i)+"\n")
	P=subprocess.Popen(cmd,stdin = subprocess.PIPE,
                     stdout = subprocess.PIPE,
                     stderr = subprocess.PIPE,
                     shell = True)
	P.stdin.close()
	P.wait()
	return  P.stdout.readlines()


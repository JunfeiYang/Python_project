#!/usr/bin/env python
#=====================================================================
# Author:Junfei Yang
# Email:yangjunfei2146@gmail.com
# File Name: 
# Description:
#
# Edit History:
#2013-03-28 File created.
#=====================================================================
import os
import os.path
import re
import subprocess
import sys

####################
#单机ping
#PING=subprocess.call(["ping","-c","3","-i","0.1","www.baidu.com"])
#PING()
#########
#循环 ping(单线程)
#for i in range(1,254):
#  PING=subprocess.call(["ping","-c","3","-i","0.1","172.16.205."+str(i)])

#PING()

##################
# 循环 ping (多线程)

for i in range(1,254):	
	subprocess.PIPE
	cmd= 'ping -c %s -i %s %s' % (3,0.01, "172.16.205."+str(i)+"\n")
	PING=subprocess.Popen(cmd,stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                shell = True)
	PING.stdin.close()
	PING.wait()
	print "execution result: %s" %PING.stdout.read()



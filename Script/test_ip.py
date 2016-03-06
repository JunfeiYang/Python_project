#!/usr/bin/env python
#========================================================================
# Author:Junfei Yang
# Email:yangjunfei2146@gmail.com
# File Name: ftp.py
# Description:
#
# Edit History:
#2013-1-26 File created.
#========================================================================
#思路: 1.到底需要pytho做什么?2.pyhton怎样调所需的命令?3.所需命令地模块加载?4.调用多线材模块;
#import subprocess

#####################################
#windows use
#cmd="cmd.exe"
#begin=101
#end=200
#while begin<end:

#subprocess.PIPE 
#p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,
#stdin=subprocess.PIPE,
#stderr=subprocess.PIPE)
#p.stdin.write("ping 192.168.1."+str(begin)+"\n")

#p.stdin.close()
#p.wait()

#print "execution result: %s"%p.stdout.read()


##########################################
#linux use 
import subprocess
import os
import os.path
begin=1
#end=10	
#cmd="`ping -c 5 -i 0.2`"
while begin<10:
	subprocess.PIPE
	cmd = 'ping -c %s %s' % (3, "172.16.236."+str(begin)+"\n")
	p = subprocess.Popen(cmd,stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                shell = True)
	p.stdin.close()
	p.wait()
	print "execution result: %s" %p.stdout.read()
	
	#
	begin = begin + 1



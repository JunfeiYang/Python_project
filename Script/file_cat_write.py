#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import sys
import os
##################
# python 语法帮助模板 sys.argv[0] 代表脚本本身; 测试时采用 print 函数;
# 例如: print sys.argv
# 注意:当脚本执行时需要两个参数,但是脚本本身也算.
if len(sys.argv) < 2:
	print "Usage: ", sys.argv[0] ," [file] [cont] "
        print  "ex: ", sys.argv[0],"  test  hello,world "
	sys.exit()
elif len(sys.argv)  < 3:
        print  "Usage: ", sys.argv[0],  " [cont]"
	print  "ex: ", sys.argv[0], " hello,world"
	sys.exit()
#########
#判断文件是否存在,存在进行下一步;否则创建;
if os.path.exists(sys.argv[1])  == True :
     print "文件存在,可以进行下一步操作 !!"
else :
     print "文件不存在,马上创建--请稍后!!!"
     #创建文件
     os.mknod(sys.argv[1])
     #创建目录
     #os.os.mkdir(sys.argv[1])
###
# 读取文件:<相当于> cat /etc/passwd
def cat_file ():
	file = '/etc/passwd'      #注意: 变量''与"" 都一样; 
	infile = open(file,"r")   #注意: infile = open("file","r")不对;"file"是字符串.
	print infile.read()
#cat_file()
def cat_w_file (file):
	ls_file = file
	infile = open(ls_file,"r")
	#print infile.read()
	cont = infile.read()
	print cont
	return cont
	
        
#写入文件: <相当于> echo "hello,world !!!" > /tmp/hello.txt
def write_file ():
	w_file = '/tmp/hello.txt'
	outfile = open(w_file,"w")
        outfile.write("hello,world!!!\n")
	outfile.close()
#write_file()
def  write_m_file (file,cont):
	w_m_file = file	
	outfile = open(w_m_file,"w")
	outfile.write(cont)
	outfile.close()
	cat_w_file(file)
# 写入内容是一行
#write_m_file(sys.argv[1],sys.argv[2])

def  write_for_file (file,cont):
	try:
          w_for_file = file	
	  outfile = open(w_for_file,"w")
	  outfile.write(cont)
        #关闭文件句柄
        finally:
	  outfile.close()
	  cat_w_file(file)

cont = cat_w_file(sys.argv[2])
write_for_file(sys.argv[1], cont)
####
#cat_w_file('/tmp/hello.txt')       
#print  sys.argv[1],sys.argv[2]

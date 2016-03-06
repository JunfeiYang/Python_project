#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os,sys
#此为pyhon学习创建文件
#待解决问题：追加内容无法换行

file_name = sys.argv[1] 
content = sys.argv[2]
#创建新文件
print file_name
def make_txt_file(file_name,content):
    if os.path.isfile(file_name):
        print "your are trying to create a file that already exists !"
    else:
        print "start create file.............\n...........\n......."
        f = open(file_name,'w')
        f.write(content)
        f.close()
        print "file already create sucessfully"
        return sys.argv[0]
#追加内容给文件
def append_txt_file(file_name,content):
  #if os.path.isfile(file_name):
    print "your are trying to create a file that already exists !"
  #else:
    print '''=============================================================\n||
    \n||\tstart append ...........\n||\t...........\n||\t.....\n==================================================================\n
          '''
    f = open(file_name,'a')
    f.write(content)
    f.close()
    print "file append sucessfully"
    return sys.argv[0]
#读取文件内容
def read_txt_file(file_name):
    f = open(file_name,'r')
    f.read()



###
#if not len(sys.argv) == 1:
#len(sys.argv)获取的数是从0开始。sys.argv[1] ==2
#if len(sys.argv) == 2:
#    print "hello"
#    read_txt_file(sys.argv[1])
#if len(sys.argv) > 3 or len(sys.argv) a< 2:
if len(sys.argv) > 3:
   print "Usage: ", sys.argv[0] ," [file_name] [content]  "
   print  "ex: ", sys.argv[0],"/tmp/test","hello,world !!!"
   sys.exit()
if len(sys.argv) < 2:
   print "Usage: ", sys.argv[0] ," [file_name]   "
   print  "ex: ", sys.argv[0],"/tmp/test"
if len(sys.argv) == 3:
   if os.path.isfile(file_name):
      append_txt_file(sys.argv[1],sys.argv[2])
      print "ok"
   else:
      make_txt_file(sys.argv[1],sys.argv[2])
      print "faile"
##
#if __name__ == '__main__':
#  make_txt_file()

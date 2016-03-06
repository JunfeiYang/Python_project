#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os,os.path,sys,re

#path=open('/var/log/system.log','r')
path=open('test/1.txt','r')
#
re_obj=re.compile(r'5')
print re_obj.finditer('5')
for line in path:
  w = re_obj.finditer(line)
  if w == 5:
     f=open('test/1.txt','a')
     f.writelines("aaa")
     f.close()
     print "插入成功"

   
   


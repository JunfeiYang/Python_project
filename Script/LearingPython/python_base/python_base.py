#!/usr/bin/env python
#-*- encoding: utf-8 -*-

#以下是python的基础练习

#1. if  and while Ture

while True:
 try:
  x=int(raw_input("please enter an integer:")) #获取行输入
  if x>0:
   print '正数'
   continue
  elif x==0:
   print '零'
   continue
  elif x<0:
   print '负数'
   continue
 except:
   print '你输入的不是整数或者你输入的已经超出了数字范围'
   break




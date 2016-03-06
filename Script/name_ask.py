#!/usr/bin/env python
#-*- encoding: utf-8 -*-
class test():
 def NAME():
  name = raw_input("what's your name ？")
  print "Hello , +name+"
 def SUDO():
  #r 原始字符串就不需要转义符了；注意不要在原始字符串的最后的一个符输入"\"
  sudout = print r'/tmp/test ll/'
 def d():
  #创建字典d,和使用
  d = dict(name='joy',age,42,sex='man',bron='hebei')
  print d['bron']
  #执行结果"hebei"
 def zidian_tmp():
    #创建字典模板，使用字典替换
    tmplate = ''' <html>
    <head><title>%(title)s</title></head>
    <body>
    <h1>%(title)s</h1>
    <p>%(text)s</p>
    </body>'''
    data = dict(title='My Home Page',text='Welcome to my home page!')
    print tmplate % data
   #执行结果：
   # <html>
   # <head><title>My Home Page</title></head>
   # <body>
   # <h1>My Home Page</h1>
   # <p>Welcome to my home page!</p>
   # </body>


if __name__ == '__main__':
     


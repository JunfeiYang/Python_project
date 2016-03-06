#!/usr/bin/env python
#__*__ coding: utf-8 __*__
import string,sys

def print_color(word):
  ''' 终端输出内容的颜色'''
  try:
   #print "ok"
   print  ''' \033[34m ====== 开始=========\n  
           str(word)
           ===========结束=============\033[0m\n
           '''
  except:
    print "脚本运行错误"

if __name__ == '__main__':
    if len(sys.argv) == 2:
     word = sys.argv[1]
     print_color(word)
    else:
      print '''\033[31m \t\t=======================
             \tusge: python sys.argv[0] str\n
              ex: python sys.argv[0] hello,word!\n
              ==========================\033[0m\n
            '''

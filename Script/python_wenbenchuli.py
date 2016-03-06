#!/usr/bin/env python
#encoding: utf-8 
# 这是一个python文本处理测试脚本
# 处理文件为当前目录test_t.txt。
#########################################
########################################
## 运行run_re_1 执行结果
## time python python_wenbenchuli.py
## LINES:: 1000001
## MATCHES:: 300
##
## real  0m1.962s
## user  0m1.929s
## sys 0m0.022s
#######################
## shell 运行结果
## time grep "5000" test_t.txt|wc -l
## 300
## real 0m0.845s
## user  0m0.834s
## sys 0m0.010s
#######################
## 运行run_re_1 执行结果
## time python python_wenbenchuli.py
## LINES:: 1000001
## MATCHES:: 300
## 
## real  0m0.564s
## user  0m0.544s
## sys 0m0.017s
##################################
######################################
import re

#定义函数run_re_1
def run_re_1():
  #匹配字符串'5000'
  pattern = '5000'
  #打开文件并且读取内容（实际操作最好加上绝对路径，本例当前路径）
  infile = open('test_t.txt','r')
  match_count = 0
  lines = 0
  for line in infile:
    match = re.search(pattern,line)
    if match:
      match_count += 1
    lines += 1
  return (lines,match_count)

#定义函数run_re_2 (这是一个编译的正则表达式，目的加快执行速度)
def run_re_2():
  #匹配字符串'5000'
  pattern = '5000'
  #创建一个编译对象
  re_obj =  re.compile(pattern)

  infile = open('test_t.txt','r')
  match_count = 0
  lines = 0
  for line in infile:
    match = re_obj.search(line)
    if match:
      match_count += 1
    lines += 1
  return (lines,match_count)

if __name__ == "__main__":
  #lines,match_count = run_re_1()
  lines,match_count = run_re_2()
  print 'LINES::',lines
  print 'MATCHES::',match_count

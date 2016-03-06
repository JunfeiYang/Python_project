#!/usr/bin/env python
#_*_ coding: utf-8 _*_
#Filename:
#function:
#Author:
#Create Date:

import glob
import os,re


#日志文件目录
v_log_dir = '/var/log'

#目标文件

#f_tab = open('test/1.txt','r')
f_tab = open('/var/log/system.log','r')


os.chdir(v_log_dir)

#查询正则表达式

#查询

#匹配以1开头后任何一个数字，相对于(1[0-9])
#p = re.compile(r'^1.')

#匹配以6开头后面可以任意多个数字
#p = re.compile(r"^6.+\d.*")

# 匹配包含”WindowServer[79]:“ 所有的行
#下面用时real 0m1.182s user  0m1.159s sys 0m0.015s
#p = re.compile(r".+.*?.WindowServer\[79\].\s.*")
#下面用时real 0m0.122s user  0m0.029s sys 0m0.010s
#p = re.compile(r"\s.*.WindowServer\[79\].\s.*")

# 完全匹配"ERROR" 使用（）
p = re.compile(r"\s.*.(ERROR).\s.*")
for v_file in f_tab:
  w = p.search(v_file)
  if w:
    # 返回被 RE 匹配的字符串默认（0)
    print w.group(0)
    #print w.start()
    #print w.end()
    #print w.span()

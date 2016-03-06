#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os,os.path
import re
import sys

if len(sys.argv) == 2:
#创建print_pdf函数
 def print_pdf(root,dirs,files):
    for file in files:
        #路径 root='/tmp',file='test'
        # '/tmp/test'
        path = os.path.join(root,file)
        #path='/tmp/test'
        #'/tmp/test'
        path = os.path.normcase(path)
        if re.search(r".*\.pdf",path):
           print path

 dir_path=sys.argv[1]
 for root,dirs,files in os.walk(dir_path):
    #for filespath in files:
      #print os.path.join(root,filespath)
      print print_pdf(root,dirs,files)
else:
    print ''' usge: sys.argv[0] /path/file
              ex:   sys.argv[0] /root/*.pdf
          '''
             

#!/usr/bin/env python
#_*_ coding: utf-8 _*_
import os, sys, shutil

def remove_dir(path,del_file):
   path = sys.argv[1]
   del_file = sys.argv[2]
   if os.path.exists(path):
     print "%s 目录存在,可以进行下一步删除操作！" % path
   else:
     print "%s 目录不存在，不需要删除" % path
     sys.exit(0)
   #print "1"
   for root,dirs,files in os.walk(path):
    #print "This print root %s" % root
    #print "This print dirs %s" % dirs
    #print "This print files %s" % files
    for d in dirs:
      #print "kk"
      #print d
      #print del_file
      if d == del_file:
        #print "jr"
        #shutil.rmtree(r'/tmp/1')
        #如果要递归删除G：\test 目录的内容，可使用shutil.rmtree()函数
        #shutil.rmtree(os.path.join(root,dirs))
        shutil.rmtree(os.path.join(root,del_file))
        if os.path.exists(path+del_file):
           print "您删除目录%s 的内容操作失败" % (path+'/'+del_file)
        else:
           print "您删除目录%s 的内容操作成功" % (path+'/'+del_file)
      #print "ok" 
      #if len(sys.argv) <= 1:
      #  print "usage: ./remove_svn path"
      #else:
      #  remove_svn(sys.argv[1])
if __name__ == '__main__':     
 if len(sys.argv) == 3:
   remove_dir(sys.argv[1],sys.argv[2])
 else:
     print         "usge: %s /path path" % sys.argv[0]
     print         "ex:   %s /tmp/ test" % sys.argv[0]
         



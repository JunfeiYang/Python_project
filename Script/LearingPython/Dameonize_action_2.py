#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
import sys

def Daemonize(stdin='/dev/null',stdout='/dev/null',stderr='/dev/null'):
          """ 创建守护进程的基类 """
          try:
            #this process would create a parent and a child
            pid = os.fork()
            #大于0，表明我们正在父进程中，等于0表示在子进程中，
            #并返回进程ID号；
            if pid > 0:
               # take care of the first parent
               sys.exit(0)
          except OSError, err:
               sys.stderr.write("Fork 1 has failed --> %d--[%s]\n" % (err.errno,err.strerror))
               sys.exit(1)
          #change to root
          #修改目录到/（一个额外的好处，是你的常驻进程不会束缚
          #住你卸载一个文件系统的能力。（如果碰巧文件系统的目录需要被卸载
          # )）
          #os.chdir('/')
          os.chdir('/tmp')
          #detach from terminal
          #从母体脱离子进程
          os.setsid()
          # file to be created ?
          #设置进程的掩码为0，最大权限，（777）
          os.umask(0)
          try:
            # this process creates a parent and a child
            pid = os.fork()
            if pid > 0:
               print "Daemon process pid %d" % pid
               #bam
               sys.exit(0)
          except OSError, err:
            sys.stderr.write("Fork 2 has failed --> %d--[%s]\n" % (err.errno,err.strerror))
            sys.exit(1)
            sys.stdout.flush()
            sys.stderr.flush()
          #The process is now dameonized,redirect standard file 
          #descriptors.
          for f in sys.stdout,sys.stderr:
            f.flush()
          si = file(stdin,'r')
          so = file(stdout,'a+')
          se = file(stderr,'a+',0)
          os.dup2(si.fileno(),sys.stdin.fileno())
          os.dup2(so.fileno(),sys.stdout.fileno())
          os.dup2(se.fileno(),sys.stderr.fileno())

##########################################################################################################
import sys,time,re,string
import os

#定义动作类
class Watchdog():
    def __init__(self, file_path='/var/log/system.log',file_size_limit=15728640):
      try:
       self.file = os.path.realpath(file_path)
       print ''' ===============================
                文件已找到，可以进行下一步操作
                =============================== '''
      except:
       assert os.path.isfile(self.file), '%s does not exist' % self.file
       print ''' ===============================
                文件没有发现，请检查确认 
                =============================== '''
      self.interval = 10
    def watch_file(self):
        #获取文件的size

        ###################
        #初始
        #file_size = os.path.getsize(self.file)
        file_size = 0
        print "这是 file_size %s " % file_size
        #################
        #增量
        current_file_size = os.path.getsize(self.file) 



        print "这是current_file %s " % current_file_size 
        if current_file_size > file_size:
           file_path='/var/log/system.log'
           v_list = open(file_path,'r')
           list1 = v_list.readlines(int(file_size))
           for i in list1:
              print "%s \n" % i
           #p = re.compile(r".*.\s.*'Yangjunfe'*.\s+.*")
           #for v_file in v_list:
           #  w = p.search(v_file)
           #  if w:
                  # 返回被 RE 匹配的字符串默认（0)
                  #       print w.group(0)
        ################################

        file_size = current_file_size
        current_size = time.sleep(10);os.path.getsize(self.file)
        print "这是再次 file_size %s " % file_size
        print "这是 current_file_size %s " % current_file_size

    def run_daemon(self):
         """Over ridden method from Daemonize.This starts the daemon."""
         while 1:
                self.watch_file()
                time.sleep(self.interval)

           

if __name__ == '__main__':
   #Daemonize(stdout='/tmp/hello.txt',stderr='/tmp/hello_erro.log')
   #print_hello()
   Daemonize(stdout='/tmp/log.txt',stderr='/tmp/log_erro.log')
   #grep_keyword('Yangjunfe kernel\[0\]:')
   Watchdog().run_daemon()

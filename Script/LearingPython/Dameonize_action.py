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
def  print_hello():
     start_time = time.time()
     end_time = start_time + 5
     while start_time < end_time:
          now = time.ctime()
          now1 = time.time()
          if int(now1) % 5 == 0:
             sys.stderr.write("Hello,world failed!%s\n"% now)
             time.sleep(5)
          else:
             sys.stdout.write("Hello,world !%s\n"% now)
             time.sleep(5)
def print_a(a):
    now = time.ctime()
    sys.stderr.write("%s:%s"% (now,a)) 
def  grep_keyword(keyword):
     k = keyword
     f_tab = open('/var/log/system.log','r')
     #f_tab = open('/tmp/test','r')
     #p = re.compile(r".*\s.*.(k).\s.*")
     p = re.compile(r".*.\s.*k*.\s+.*")
     for v_file in f_tab:
         w = p.search(v_file)
         if w:
            # 返回被 RE 匹配的字符串默认（0)
            print w.group(0)
#pool = str(grep_keyword('WindowServer\[348\]'))
#print pool
def action_start(grep_keyword):
     #pool = str(grep_keyword('Yangjunfe kernel\[0\]:'))
     pool = str(grep_keyword('WindowServer\[348\]'))
     while 1:
         
      now = time.ctime()
      #try:
      for i in pool:
              try:
              #sys.stdin.readlines(i)
                sys.stdout.write(i,'a')
              #print "操作成功 %s\n" % now
              #time.sleep(10)
      #except:
              #pass
              except:
                sys.stderr.write("操作失败%s\n" % now)
              #time.sleep(10)
                break
if __name__ == '__main__':
   #Daemonize(stdout='/tmp/hello.txt',stderr='/tmp/hello_erro.log')
   #print_hello()
   #Daemonize(stdout='/tmp/log.txt',stderr='/tmp/log_erro.log')
   #grep_keyword('Yangjunfe kernel\[0\]:')
   #action_start(grep_keyword)
   print_a("aaa")

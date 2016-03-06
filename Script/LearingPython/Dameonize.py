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
            #sys.stdout.flush()
            #sys.stderr.flush()
          #The process is now dameonized,redirect standard file 
          #descriptors.
          for f in sys.stdout,sys.stderr:
            f.flush()
          si = file(stin,'r')
          so = file(stdout,'a+')
          se = file(stderr,'a+',0)
          os.dup2(si.fileno(),sys.stdin.fileno())
          os.dup2(so.fileno(),sys.stdout.fileno())
          os.dup2(se.fileno(),sys.stderr.fileno())

##########################################################################################################

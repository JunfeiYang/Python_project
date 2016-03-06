#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
import sys

class Daemonize:
   """ 创建守护进程的基类 """
   def daemonize(self):
          try:
            #this process would create a parent and a child
            pid = os.fork()
            if pid > 0:
               # take care of the first parent
               sys.exit(0)
          except OSError, err:
               sys.stderr.write("Fork 1 has failed --> %d--[%s]\n" % (err.errno,err.strerror))
               sys.exit(1)
          #change to root
          #os.chdir('/')
          os.chdir('/tmp')
          #detach from terminal
          os.setsid()
          # file to be created ?
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
   def start_daemon(self):
    self.daemonize()
    #self.run_daemon()


   def run_daemon(self):
    """override"""
    pass

##########################################################################################################
import time

class Print_Hello(Daemonize):
    def __init__(self, file_path, size_limit=15728640):
       self.file = os.path.realpath(file_path)
       print '---'
       #assert 语句用来声明某个条件是真的（前提在你非常确信的基础）
       assert os.path.isfile(self.file), '%s does not exist' % self.file
       print '+++'
       self.userhome = os.getenv('HOME')
       self.file_size_limit = size_limit
       self.interval = 3600
       self.log_file = os.path.join(self.userhome, '/tmp/print_hello.log')
    
    def watch(self):
        current_file_size = os.path.getsize(self.file)
        if current_file_size > self.file_size_limit:
           #self.send_an_email()
           f = open(self.log_file, 'a')
           f.write('Last checked on : %s' % time.asctime(time.localtime(time.time())))
           f.write('\n')
           f.close()
    def run_daemon(self):
       """Over ridden method from Daemonize.This starts the daemon."""
       while 1:
             self.watch()
             time.sleep(self.interval)

if __name__ == '__main__':
    watchdog = Print_Hello('/tmp/test')
    watchdog.start_daemon()
    #watchdog.run_daemon()

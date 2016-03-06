#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import string, threading, time, string ,subprocess

################################################
# 加入Queue 使线程更为简单化，因为队列模块通过信号量的使用会
# 明显减轻数据的保护需要，队列本身已经是通过内部的一个信号量
# 进行保护了。
##############################################

from Queue import Queue

###################
# 在Python中线程和队列的基本关系中。当队列为空时工作完成。
##############
queue=Queue() #创建队列

####
Milti_action = ["ping -c 3 baidu.com",
                "echo 'hello,world!'",
                "ifconfig -a",
                "uname -a",
                "whoami"]
############
#action （1..n)
def action(a,q):
    ''' Multi-action；'''
    while True:
      cmd=q.get()
      #cmd= 'ping -c %s %s' % (2,"baidu"+".com"+"\n")
      ret=subprocess.call(cmd,stdin = subprocess.PIPE,
                                shell = True,
                                stdout = open('/dev/null','w'),
                                stderr=subprocess.STDOUT)
      if ret == 0:
       print "execution result(执行结果): %s" % cmd
      else:
       print "%s: did not respond" % cmd
      queue.task_done()  

      #time.sleep(1)

print Milti_action
#########################
#def thread_main(x):
    #global count, mutex
    # 获得线程名
    #threadname = threading.currentThread().getName()
    #print x # x 为1、2、3、4、5
    #for j in Milti_action:
    #  print action(j)
    #print threadname

    
def main(num):
    threads = []
    
    threadname = threading.currentThread().getName()
    # 先创建线程对象
    for x in xrange(1, num+1):
        threads.append(threading.Thread(target=action, args=(x,queue)))
    # 启动所有线程
    for t in threads:
        t.setDaemon(True)
        t.start()
        time.sleep(0.1)
    for j in Milti_action:
      queue.put(j)
    # 主线程中等待所有子线程退出
   # for t in threads:
   #     t.join() 
    print "Main Thread Wating"
    queue.join()
    print "Done"
    
    
if __name__ == '__main__':
    num = len(Milti_action)
    # 创建工作需要的线程个数
    main(num)

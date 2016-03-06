#!/usr/bin/env python
#-*- encoding: utf-8 -*-
######################
# 描述：
#  此模板为发挥python 多线程优势创建
#  多线程可以节省资源，（例如：创建多个任务，一些使用硬盘资源
#  一些使用网络资源。可以更高提高资源利用）
################################

import string, threading, time, string ,subprocess, re

################################################
# 加入Queue 使线程更为简单化，因为队列模块通过信号量的使用会
# 明显减轻数据的保护需要，队列本身已经是通过内部的一个信号量
# 进行保护了。
# q = Queue.Queue ; q.gett(self, block=True, timeout=None)
# None可以换成时间（秒）；
##############################################

from Queue import Queue

###################
# 在Python中线程和队列的基本关系中。当队列为空时工作完成。
##############
in_queue=Queue() #创建队列
out_queue=Queue()
####
Milti_action1 = [" baidu",
                "google",
                "sina",
                "apple",
                "yahoo"]
####
Milti_action2 = ['uname -a',
                 'ifconfig -a',
                'date']
############
#action （1..n)
def action_ping(i,iq):
    ''' Multi-action；'''
    while True:
      ip =iq.get()
      print "Thread %s: pinging %s" %(i,ip)
      #cmd= 'ping -c %s %s' % (2,"baidu"+".com"+"\n")
      ret=subprocess.call("ping -c 3 %s" % ip,
                                shell = True,
                               # stdout = open('/dev/null','w'),
                                stderr=subprocess.STDOUT)
      
      if ret == 0:
       print "execution result(执行结果): %s\n" % ret
       #oq.put(ip)
      else:
       print "%s: did not respond\n" % ret
      iq.task_done()  

      #time.sleep(1)

#print Milti_action
#########################
#action 2 :uname -a
def action_show_system(i,oq):
    '''查看系统类型'''
    #使进程陷入死循环，直到执行完毕
    while True:
      cmd=oq.get()
      p=subprocess.call(cmd,
                         shell = True)
      if p == 0:
        print "执行结果：%s\n" % p
      else:
        print "任务没有反应：%s\n" % p
      oq.task_done()
      
def main(num):
    threads = []
    
    threadname = threading.currentThread().getName()
    # 先创建线程对象
    for x in xrange(1, num+1):
        #target后面代表目标的名字，args后代表目标的形参。
        threads.append(threading.Thread(target=action_ping, args=(x,in_queue)))
        threads.append(threading.Thread(target=action_show_system, args=(x,out_queue)))
    # 启动所有线程
    for t in threads:
        t.setDaemon(True)
        t.start()
        time.sleep(0.1)
    #循环Milti_action1
    for j in Milti_action1:
      in_queue.put(j)
    #循环Milti_action2
    for k in Milti_action2:
      out_queue.put(k)
    # 主线程中等待所有子线程退出
   # for t in threads:
   #     t.join() 
    print "Main Thread Wating"
    in_queue.join()
    out_queue.join()
    print "Done"
    
    
if __name__ == '__main__':
    #num = len(Milti_action1)
    num = 5
    # 创建工作需要的线程个数
    main(num)

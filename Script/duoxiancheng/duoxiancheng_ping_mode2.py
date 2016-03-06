#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import string, threading, time, string ,subprocess

# 函数主要在于 return 返回值
#def address_domain():
#    all=['baidu','sina','yahoo','sohu','apple'] 
#    return all
key = ['baidu','sina','yahoo','sohu','apple'] 
#print address_domain()
##############
#action 1
def ping(p):
      subprocess.PIPE
      cmd= 'ping -c %s %s' % (2,str(p)+".com"+"\n")
      PING=subprocess.Popen(cmd,stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                shell = True)
      PING.stdin.close()          
      PING.wait()                 
      print "execution result: %s" %PING.stdout.read()
      #time.sleep(1)
#######################
    #
#x,key形参，x为创建对象时循环的变量。key为列表。    
def thread_main(x,key):
    #global count, mutex
    # 获得线程名
    threadname = threading.currentThread().getName()
    #print threadname
    #主要作用相当触发器，pop方法会移除key列表中的一个元素
    #默认是最后一个,并返回该元素的值·
    #
    a = key.pop()
    print a
    ping(a)
    print threadname
    
def main(num):
    threads = []
    
    # 先创建线程对象
    for x in xrange(1, num+1):
      threads.append(threading.Thread(target=thread_main, args=(x,key)))
    # del key[1]
    # 启动所有线程
    for t in threads:
        t.setDaemon(True)
        t.start()
        #sleep可以使线程全部工作
        time.sleep(0.1)
    # 主线程中等待所有子线程退出
    for t in threads:
        t.join()  

if __name__ == '__main__':
    num = 5
    # 创建4个线程
    main(num)

#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import string, threading, time, string ,subprocess

# 函数主要在于 return 返回值
#def address_domain():
#    all=['baidu','sina','yahoo','sohu','apple'] 
#    return all
#print address_domain()
##############
#action 1
def ping_baidu():
      subprocess.PIPE
      cmd= 'ping -c %s %s' % (2,"baidu"+".com"+"\n")
      PING=subprocess.Popen(cmd,stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                shell = True)
      PING.stdin.close()          
      PING.wait()                 
      print "execution result: %s" %PING.stdout.read()
      #time.sleep(1)
#######################
#action 2
def ping_sina():
      subprocess.PIPE
      cmd= 'ping -c %s %s' % (2,"sina"+".com"+"\n")
      PING=subprocess.Popen(cmd,stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                shell = True)
      PING.stdin.close()          
      PING.wait()                 
      print "execution result: %s" %PING.stdout.read()
      #time.sleep(1)
########################
#action 3
def ping_yahoo():
      subprocess.PIPE
      cmd= 'ping -c %s %s' % (2,"yahoo.com"+"\n")
      PING=subprocess.Popen(cmd,stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                shell = True)
      PING.stdin.close()          
      PING.wait()                 
      print "execution result: %s" %PING.stdout.read()
      #time.sleep(1)

#########################
#action 4
def ping_sohu():
      subprocess.PIPE
      #cmd= 'ping -c %s %s' %(2,"sohu"+".com"+"\n")
      cmd= 'ping -c %s  %s'  % (3, 'sohu.com'+"\n")
      PING=subprocess.Popen(cmd,stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                shell = True)
      PING.stdin.close()          
      PING.wait()                 
      print "execution result: %s" %PING.stdout.read()
      #time.sleep(1)

#########################
#action 5
def ping_apple():
      subprocess.PIPE
      cmd= 'ping -c %s %s' % (2,"apple.com"+"\n")
      #cmd='echo %s'%("hello,world")
      PING=subprocess.Popen(cmd,stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                shell = True)
      PING.stdin.close()          
      PING.wait()                 
      print "execution result: %s" %PING.stdout.read()
      #time.sleep(1)

#########################
def thread_main1(a):
    #global count, mutex
    # 获得线程名
    threadname = threading.currentThread().getName()
    #print threadname
    #
    ping_baidu()

def thread_main2(a):
    #global count, mutex
    # 获得线程名
    threadname = threading.currentThread().getName()
    #print threadname
    #
    ping_yahoo()
    #
def thread_main3(a):
    #global count, mutex
    # 获得线程名
    threadname = threading.currentThread().getName()
    #print threadname
    ping_sohu()
    #
def thread_main4(a):
    #global count, mutex
    # 获得线程名
    threadname = threading.currentThread().getName()
    #print threadname
    ping_sina()
    #
def thread_main5(a):
    #global count, mutex
    # 获得线程名
    threadname = threading.currentThread().getName()
    #print threadname
    ping_apple()
    
def main(num):
    threads = []
    
    # 先创建线程对象
    for x in xrange(1, num+1):
        #
        threads.append(threading.Thread(target=thread_main1, args=(x,)))
        #
        threads.append(threading.Thread(target=thread_main2, args=(x,)))
        #
        threads.append(threading.Thread(target=thread_main3, args=(x,)))
        #
        threads.append(threading.Thread(target=thread_main4, args=(x,)))
        #
        threads.append(threading.Thread(target=thread_main5, args=(x,)))
    # 启动所有线程
    for t in threads:
        t.setDaemon(True)
        t.start()
        time.sleep(0.1)
    # 主线程中等待所有子线程退出
    for t in threads:
        t.join()  
    
    
if __name__ == '__main__':
    num = 5
    # 创建4个线程
    main(num)

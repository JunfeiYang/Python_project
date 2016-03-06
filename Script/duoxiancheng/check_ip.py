#!/usr/bin/env python
#-*- encoding: utf-8 -*-
#=====================================================================
# Author:Junfei Yang
# Email:yangjunfei2146@gmail.com
# File Name: 
# Description:
#
# Edit History:
#2013-03-28 File created.
#=====================================================================
import string, threading, time
import subprocess, sys

def ping(p):
    subprocess.PIPE
    #ping -c <次数> -i <频率> -W <等待时间>
    #cmd= 'ping -c %s -i %s -W %s %s'  % (3,0.2,1, "172.16.205."+str(p)+"\n")
    cmd= 'ping -c %s -W %s %s'  % (3,1, "172.16.205."+str(p)+"\n")
    PING=subprocess.Popen(cmd,stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                shell = True)
    PING.stdin.close()          
    #PING.wait()                 
    print "execution result: %s" %PING.stdout.read()


def thread_main(a):
    # 获得线程名
    threadname = threading.currentThread().getName()
    
    #print threadname
    ping(a)
    
def main(num):
    threads = []
    
    # 先创建线程对象
    for x in xrange(1, num+1):
        threads.append(threading.Thread(target=thread_main, args=(x,)))
    # 启动所有线程
    for t in threads:
        t.setDaemon(True)
        t.start()
        time.sleep(0.1)
	      #保证线程全部启动
    # 主线程中等待所有子线程退出
    for t in threads:
        t.join()  
    
if __name__ == '__main__':
    num = 254
    
    # 创建4个线程
    main(num)

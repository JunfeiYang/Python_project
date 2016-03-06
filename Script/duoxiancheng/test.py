#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import string, threading, time
import subprocess, sys

def ping(p):
    subprocess.PIPE
    cmd= 'ping -c %s -i %s %s' % (3,0.01, "172.16.205."+str(p)+"\n")
    PING=subprocess.Popen(cmd,stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                shell = True)
    PING.stdin.close()          
    PING.wait()                 
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
        t.start()
    # 主线程中等待所有子线程退出
    for t in threads:
        t.join()  
    
    
if __name__ == '__main__':
    num = 254
    # 创建4个线程
    main(num)

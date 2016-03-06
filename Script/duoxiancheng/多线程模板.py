#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import string, threading, time

def thread_main(a):
    global count, mutex
    # 获得线程名
    threadname = threading.currentThread().getName()
    
    print threadname
    time.sleep(1)
    
def main(num):
    threads = []
    
    # 先创建线程对象
    for x in xrange(0, num):
        threads.append(threading.Thread(target=thread_main, args=(10,)))
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

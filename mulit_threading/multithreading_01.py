import threading,time
import os,sys
from concurrent.futures import ThreadPoolExecutor #线程池，进程池

#  标准库为我们提供了 concurrent.futures 模块，它提供了 
# ThreadPoolExecutor (线程池)和ProcessPoolExecutor (进程池)两个类。

def test(arg):
    print(arg,threading.current_thread().name)
    time.sleep(0.1)

if __name__ == "__main__":
    thread_pool = ThreadPoolExecutor(10) #定义5个线程执行此任务
    
    for i in range(100):
        thread_pool.submit(test,i)

# 前言

   从Python3.2开始，标准库为我们提供了 concurrent.futures 模块，
它提供了 ThreadPoolExecutor (线程池)和ProcessPoolExecutor (进程池)两个类。
相比 threading 等模块，该模块通过 submit 返回的是一个 future 对象，
它是一个未来可期的对象，通过它可以获悉线程的状态主线程(或进程)中可以获取某一个线程(进程)执行的状态或者某一个任务执行的状态及返回值：



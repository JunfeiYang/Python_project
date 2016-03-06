#!/usr/bin/env python
#coding=utf8

import threading,subprocess,time

###################
def ping_local():
    subprocess.PIPE
    cmd= 'ping -c %s %s' % (1,"127.0.0.1"+"\n")
    PING=subprocess.Popen(cmd,stdin = subprocess.PIPE,
                              stdout = subprocess.PIPE,                                                  stderr = subprocess.PIPE,
                              shell = True)
    print "127.0.0.1 ping_local"
    PING.stdin.close()          
    PING.wait()                 
    print "execution result: %s" %PING.stdout.read()
##########

def main(num):
    
    threadss = [] 
    '''
    threadlist = ['ping_baidu','ping_google','ping_yahoo',
                  'ping_amzon',
                  'ping_sina']
    '''  
    threadlist = ['ping_local','ping_local']
   # 先创建线程对象
    for ip in threadlist:
        #print ip
        #threads.append(threading.Thread(target=thread_main, args=(ip,)))
        #threading.Thread(target=ip)
        threadss.append(threading.Thread(target=ip))
        #t=threading.Thread(target=ip)
        print threadss
#       print threading.Thread(target=ip)
        #print threadss
   # 启动所有线程
    for t in threadss:
#        t.setDaemon(True)     
        t.start()
#   # 主线程中等待所有子线程退出
#        time.sleep(0.1)
#    for t in threadss:
#        t.join()
if __name__ == '__main__':
        num = 10
        # 创建10个线程
        main(num)
    
#创建两个线程
#t = threading.Thread(target=loop)
#t2 = threading.Thread(target=loop2)
#线程开始运行
#t.start()
#t2.start()
#线程挂起，直到线程结束
#t.join()
#t2.join()


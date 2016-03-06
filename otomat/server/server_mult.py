#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import os
import time
import sys
import traceback
import socket
from otomat.conf import conf
from threading import *

#
class active_server:
    def __init__(self, filename=None):
        self.filename = filename
        cnf = conf.files_conf_check(self.filename)
        self.port = cnf.server_port()
        self.ip = cnf.server_ip()
        # 线程池
        self.MAXTHREADS = 5
        self.lockpool = Lock()
        self.busylist = {}
        self.waitinglist = {}
        self.queue = []
        self.sem = Semaphore(0)

    def handleconnection(self, clientconn):
        """ 处理进来的连接"""
        self.lockpool.acquire()
        print "Received new client connection"
        print "Got connection from ", clientconn.getpeername()
        try:
            print 'waitinglist is : %s' % len(self.waitinglist)
            print "buyslist is: %s" % len(self.busylist)
            print "activeCount is : %s" % (activeCount()-1)
            print "Maxthereads is : %s" % self.MAXTHREADS
            if len(self.waitinglist) == 0 and (activeCount()-1) >= self.MAXTHREADS:
                # 如果超出连接,立即关闭它.
                clientconn.close()
                return
            if len(self.waitinglist) == 0:
                self.startthread()


            self.queue.append(clientconn)
            self.sem.release()
        finally:
            self.lockpool.release()

    def startthread(self):
        """接着客户端socket被加入队列(queue)中,同时semaphore被释放--通知处理线程有可用的新连接
        最后,线程池锁被释放. """
        print "Starting new client processor thread"
        t = Thread(target=self.threadworker())
        t.setDaemon(1)
        t.start()
    def threadworker(self):
        #time.sleep(1)  # Simulate expensive startup
        print "I'm here !  This is threadworker begin"
        name = currentThread().getName()
        print "I went  to here : %s" % name
        self.lockpool.acquire()
        try:
            #self.lockpool.acquire()
            print self.waitinglist()
            self.waitinglist[name] = 1
            #try:
             #   print "Hello world !"
             #   self.waitinglist[name] = 1
            #finally:
                #self.lockpool.release()
            print  "I went to here processclients"
            self.processsclients()
        finally:
            # clean up if the thread is dying for some reason.
            # Can't lock here -- we may already hold the lock, but it's OK .
            self.lockpool.release()
            print "** WARNING ** Thread %s died" % name
            if name in self.waitinglist:
                del self.waitinglist[name]
            if name in self.busylist:
                del self.busylist[name]
            # Start a replacement thread.
            self.startthread()
    def processclients(self):
        """ Main loop of client-processing threads."""
        print "I went to here , processclients begin"
        name = currentThread().getName()
        while True:
            self.sem.acquire()
            self.lockpool.acquire()
            try:
                clientconn = self.queue.pop(0)
                print  clientsock
                del self.waitinglist[name]
                self.busylist[name] = 1
            finally:
                self.lockpool.release()
            try:
                print "[%s] Got connection from %s" % (name, clientsock.getpeername())
                clientsock.sendall("Greetings. You are being serviced by %s.\n" % name)
                while True:
                    data = clientconn.recv(4096)
                    if data.startswith('DIE'):
                        sys.exit(0)
                    if not len(data):
                        break
                clientconn.sendall(data)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                traceback.print_exc()
            # Close the connection
            try:
                clientconn.close()
            except KeyboardInterrupt:
                raise
            except:
                trackeback.print_exc()
            self.lockpool.acquire()
            try:
                del self.buyslist[name]
                self.waitinglist[name] = 1
            finally:
                self.lockpool.release()

    def listener(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        #print self.ip
        #print self.port
        s.bind((self.ip, int(self.port)))
        s.listen(1)
        while True:
            try:
               (clientconn, clientaddr) = s.accept()
            except (KeyboardInterrupt, SystemExit):
                #print "you have CTRL+C,Now quit"
                raise
            except:
                traceback.print_exc()
                continue
            #print "it's ok"
            self.handleconnection(clientconn)


def main(f):
    t = active_server(f)
    t.listener()
if __name__ == "__main__":
    main("otomat.cnf")

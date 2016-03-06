#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os
import time
import sys
import traceback
import os
import socket
from otomat.conf import conf
from threading import *

#
class active_server:
	def __init__(self, filename=None):
		self.filename = filename
		cnf = conf.files_conf_check(self.filename)
		self.port = cnf.server_port()
		self.host = cnf.server_ip()
		#ThreadPool
		self.MaxThreads = 5
		self.lockpool = Lock()
		#self.queue = []
		self.sem = Semaphore(0)
	def  handleconnection(self,clientconn):
		"""handle an incoming connection."""
		print "Received new Client connection."
		try:
			print "Got connection from", clientconn.getpeername()
			if (active_count()-1) >= self.MaxThreads:
			# Too many connections. Just close it and exit
				clientconn.close()
				return
			'''Main loop of client-process threads.'''	
			name = current_thread().getName()
			clientconn.sendall('Greetings. You are being serviced by recviled' )
			while True:
				data = clientconn.recv(4096)
				if  not len(data):
					break
				clientconn.sendall(data)
		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			traceback.print_exc()
		#close the connection
		try:
			clientconn.close()
		except KeyboardInterrupt:
			raise
		except:
			traceback.print_exc()

	def  startthread(self):
		# Called by handleconnection when a new thread is need.
		# Note:lockpool is already acquired when this fuction is called.
		print "Starting netw Client processor thread."
		t = Thread(target = self.handleconnection(),args = [clientconn])
		t.setDaemon(1)
		t.start()

	def listener(self):
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		s.bind((self.host,int(self.port)))
		s.listen(5)
		while True:
			try:
				clientconn, clientaddr = s.accept()
			except (KeyboardInterrupt,SystemError):
				raise
			except:
				traceback.print_exc()
				continue
			self.handleconnection(clientconn)

def main(f):
	t = active_server(f)
	t.listener()
if __name__ == "__main__":
	main("otomat.cnf")

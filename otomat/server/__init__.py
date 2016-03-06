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
from Queue import Queue
from otomat.plugins import pysql
from  otomat.logs  import log as logging
queue=Queue() #create queue
#
config =conf.otomat_conf('/etc/otomat/otomat.cnf')
logfile = config.server_log()
logdir = config.server_logdir()

if not os.path.exists(logdir):
        os.makedirs(logdir,0o755)

os.chdir(logdir)
logging.set_logger(filename =logfile, mode = 'a')


'''
class recive_report:
	def __init__(self,report_file = "/tmp/report",filename = None,data= None):
		#self.filename = filename
		#cnf = conf.otomat_conf(self.filename)
		#self.path = config.server_report_path()
		self.report = report_file
		self.data = data
	def  report(self):
		print self.report
		print self.data
		#os.chdir(self.path)
		f = open(self.report,'w+')
		f.writelines(self.data)
		traceback.print_exc()
		f.close()
'''


#

class active_server:
	def __init__(self, filename="otomat.cnf"):
		#recive_report.__init__(self)
		self.filename = filename
		config = conf.otomat_conf(self.filename)
		self.port = config.server_port()
		self.host = config.server_host()
		self.sql_host = config.db_host()
		self.sql_user = config.db_user()
		self.sql_password = config.db_password()
		self.sql_defdb = config.db_defaultdb()
		#ThreadPool
		self.MaxThreads = config.server_worker()
		#self.lockpool = Lock()
		#self.queue = []
		#self.sem = Semaphore(0)
	def  handleconnection(self,clientconn):
		"""handle an incoming connection."""
		logging.info("Received new Client %s connection.",  clientconn.getpeername())
		try:
			logging.debug("Got connection from %s",  clientconn.getpeername())
			if (active_count()-1) >= self.MaxThreads:
				clientconn.close()
				return
			"""Main loop of client-process threads."""
			name = current_thread().getName()
			clientconn.sendall('Greetings. You are being serviced by recviled' )
			while True:
				data = clientconn.recv(4096)
				if  not len(data):
					logging.info(("The client data has been received and connection will be disconected!"))
					break

				clientconn.sendall(data)
				recv_data = eval(data)
				#print   data
				print recv_data
				logging.debug(data)
				self.insert_data(recv_data)
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
		logging.info(("Starting netw Client processor thread."))
		global queue
		threads = []
		pool = self.MaxThreads
		t = Thread(target = self.handleconnection(),args = (clientconn,queue))
		for x in xrange(1, pool+1):
			threads.append(t)
		for i in threads:
			t.setDaemon(1)
			t.start()
			#time.sleep(0.1)
		#queue.join()
       	# write data for file
	"""
	def  report(self,data):

	        f = open('/tmp/report',"ab")
	        try:
		    f.writelines(data)
	        except IOError:
		    traceback.print_exc()
	        finally:
		    f.close()
	"""
    	def insert_data(self,recv_data):
		data = recv_data
        	insert = pysql.pysql(data)
        	logging.debug(insert)
		return insert
	def listener(self):
        	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		s.bind((self.host,int(self.port)))
		s.listen(5)
		logging.info(("The otomat-server has been launched successfully "))
		while True:
			try:
				clientconn, clientaddr = s.accept()
			except (KeyboardInterrupt,SystemError):
				raise
				logging.error(("The otomat-server start  failure"))
			except:
				traceback.print_exc()
				logging.error(trackback.print_exc())
				logging.error(("The otomat-server start  failure"))
				continue
			self.handleconnection(clientconn)




#if __name__=="__main__":
#	data = '''
#	Welcome to china  lllllllllllllllllllllllllllll
#	'''
#	report(data)
#	#t = recive_report(data)
#	#t.report()

def main(argv=sys.argv[1:]):
	t1 = active_server(argv)
	t1.listener()
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))


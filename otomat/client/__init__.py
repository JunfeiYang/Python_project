#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os,re
import time
import sys
#import StringIO
import socket
#import pickle
from otomat.conf  import  conf  
from otomat.plugins import cpu
from otomat.plugins import disk
from otomat.plugins import mem
from otomat.plugins import network
from otomat.plugins import hostname
from otomat.plugins import login_user
from otomat.plugins import ip_address
from otomat.logs import log as logging


config = conf.otomat_conf('/etc/otomat/otomat.cnf')
logfile = config.client_log()
logdir = config.client_logdir()
if not os.path.exists(logdir):
	os.makedirs(logdir,0o755)
#print logfile
#print logdir
os.chdir(logdir)
logging.set_logger(filename =logfile, mode = 'a')

#
def os_release():
 	s = []
	f = open ('/etc/issue')
	s = f.read()
	return s.split()[0]
'''
def os_release_centos():
        s = []
        f = open('/etc/redhat-release')
        s = f.read()
        return s.split()[0]
'''
class active_agent:
    def __init__(self, filename = '/etc/otomat/otomat.cnf'):
	    self.filename = filename
	    config = conf.otomat_conf(self.filename)
	    self.port = config.server_port()
	    self.host = config.server_host()
	    self.client_nic = config.nic_port()
	    #print self.port
	    #print self.host
    def handleconnection(self):
		try:
			data = str(self.transnit_data())
			#data = 'test'
			print data
			logging.info(("Otomat agent started Successfully!"))
			while True:
                                try:
				    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				    s.connect((self.host,int(self.port)))
				    logging.info(("Otomat agent has been successfully connected to the server!!"))
				    s.sendall(data)
				    logging.debug(data)
				    buf = s.recv(8092)
				    if not len(data): break
				    s.close()
                                except:
                                        continue
                                        logging.error('socket.error: [Errno 111] Connection refused')
                                finally:
				    time.sleep(300)
		except:
			logging.error('The socket connect to the server failed!!!')
    def transnit_data(self):
        data = {}
        # cpu
        cpu_loadavg = cpu.cpu_loadavg()
        cpu_user = cpu.cpu_user()
        cpu_nice = cpu.cpu_nice()
        cpu_system = cpu.cpu_system()
        cpu_iowait = cpu.cpu_iowait()
        cpu_steal = cpu.cpu_steal()
        cpu_idle = cpu.cpu_idle()
		# mem
        mem_total =  mem.mem_total()
        mem_freed =  mem.mem_freed()
        mem_used = mem.mem_used()
        mem_buffers_freed = mem.mem_buffers_freed()
        mem_buffers_used = mem.mem_buffers_used()
        mem_used_percent = mem.mem_used_percent()
        swap_total = mem.swap_total()
        swap_freed= mem.swap_freed()
        swap_used = mem.swap_used()
        swap_used_percent = mem.swap_used_percent()
		# disk  
        disk_total = disk.disk_total()
        disk_freed = disk.disk_freed()
        disk_used = disk.disk_used()
        disk_used_percent = disk.disk_used_percent()
		# network nic I/O
        networktraffic_recv = network.nic_traffic_recv()
        networktraffic_sent = network.nic_traffic_sent()
        networktraffic_recv_error = network.nic_traffic_recv_err()
        networktraffic_sent_error = network.nic_traffic_sent_err()
        '''
        if os_release() == "Ubuntu":
            network_recv = collect.nic_io_ubuntu().bytes_recv
            network_sent = collect.nic_io_ubuntu().bytes_sent
            elif os_release() == "CentOS ":
            network_recv = collect.nic_io_centos().bytes_recv
            network_sent = collect.nic_io_centos().bytes_sent
        else:
            pass
        print network_recv
        '''
		# hostname and ipaddress
        host = hostname.hostname_get()
        #ifname = self.client_nic
        ip = ip_address.ip_address()
		# login user num
        login_user_name = login_user.login_user_name()
        login_user_num = login_user.login_user_num()
		#print ip_address
		#ip_address = '172.16.209.243'
		#
        L1 = ['cpu_loadavg','cpu_user','cpu_nice','cpu_system','cpu_iowait',
                'cpu_steal','cpu_idle','mem_total','mem_freed','mem_used',
                'mem_buffers_freed','mem_buffers_used','mem_used_percent',
                'swap_total','swap_freed','swap_used','swap_used_percent',
                'disk_total','disk_freed','disk_used','disk_used_percent',
                'networktraffic_recv','networktraffic_sent','networktraffic_recv_error',
                'networktraffic_sent_error','hostname','host_ip','login_user_name','login_user_num']
        L2 = [cpu_loadavg,cpu_user,cpu_nice,cpu_system,cpu_iowait,
                cpu_steal,cpu_idle,mem_total,mem_freed,mem_used,
                mem_buffers_freed,mem_buffers_used,mem_used_percent,
                swap_total,swap_freed,swap_used,swap_used_percent,
                disk_total,disk_freed,disk_used,disk_used_percent,
                networktraffic_recv,networktraffic_sent,networktraffic_recv_error,
                networktraffic_sent_error,host,ip,login_user_name,login_user_num]


        data = dict(zip(L1[::],L2))
        #print data
        #data = 'hello,word'
        return data
        logging.debug('%s is flow:' % data )





#if __name__=="__main__":

#	t = active_agent()
#	t.transnit_data()


def main(argv=sys.argv[1:]):
    t = active_agent(argv)
    t.handleconnection()
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

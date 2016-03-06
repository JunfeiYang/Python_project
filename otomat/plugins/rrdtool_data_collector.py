#_*_ coding: UTF-8 _*_
import sys,time,os
reload(sys)
sys.setdefaultencoding('utf8')
import rrdtool
import random
import time
import MySQLdb
import shell_cmd as shell
from otomat.conf import conf
from otomat.logs import log as logging
from MySQLdb import converters

config =conf.otomat_conf('/etc/otomat/otomat.cnf')
logfile = config.report_log()
logdir = config.server_logdir()

if not os.path.exists(logdir):
        os.makedirs(logdir,0o755)

os.chdir(logdir)
logging.set_logger(filename =logfile, mode = 'a')

class rrdtool_collector:
    """
    rrdtool 绘图过程一共有四步：
    1.创建rrdtool数据库
    2.插入rrdtool所需的数据
    3.更新rrdtool数据库
    4.进行rrdtool绘图。
    """
    def __init__(self,filename="/etc/otomat/otomat.cnf",graph=None,title="北京壹號車 系統報告"):
        self.filename = filename
	config = conf.otomat_conf(self.filename)
	# rrdtool
	self.rrdtool_cpu = config.rrdtool_cpu()
	self.rrdtool_mem = config.rrdtool_mem()
	self.rrdtool_disk = config.rrdtool_disk()
	self.rrdtool_host = config.rrdtool_host()
	self.rrdtool_network = config.rrdtool_nic()
	self.rrdtool_dir = config.rrdtool_dir()
	self.rrdtool_login = config.rrdtool_login()
	# sql
	self.host = config.db_host()
	self.user = config.db_user()
	self.password = config.db_password()
	self.defaultdb = config.db_defaultdb()
        #self.time = str(int(time.time()))
    def rrdb(self):
        """
        1.创建rrdtool的数据库.
        """
        cur_time = str(int(time.time()-3000))
        #cur_time = '1417652469'
	host = self.rrdtool_host
	#print host
	report_dir = self.rrdtool_dir
	#print report_dir
	report_rrd = [self.rrdtool_cpu,self.rrdtool_mem,self.rrdtool_disk,self.rrdtool_network,self.rrdtool_login]
	#print report_rrd
	if not os.path.exists(report_dir):
		os.mkdir(report_dir)
	for i in list(host.split(',')):
		os.chdir(report_dir)
		if not os.path.exists(i):
			os.mkdir(i)
		os.chdir(i)
		for j in report_rrd:
		#	if not os.path.exists(j):
		#		os.mknod(j)
			if not os.path.exists('nic.rrd'):
				# network_db
				rrdtool.create('nic.rrd','--step','300','--start',cur_time,
        				'DS:input:COUNTER:600:0:U',
        				'DS:output:COUNTER:600:0:U',
        				'DS:input_err:COUNTER:600:0:U',
        				'DS:output_err:COUNTER:600:0:U',
       					'RRA:LAST:0.5:1:600',
       					'RRA:LAST:0.5:6:700',
       					'RRA:LAST:0.5:24:775',
       					'RRA:LAST:0.5:288:797',
       					'RRA:MAX:0.5:1:600',
       					'RRA:MAX:0.5:6:700',
       					'RRA:MAX:0.5:24:775',
       					'RRA:MAX:0.5:288:797',
       					'RRA:MIN:0.5:1:600',
       					'RRA:MIN:0.5:6:700',
       					'RRA:MIN:0.5:24:775',
       					'RRA:MIN:0.5:288:797',
       					'RRA:AVERAGE:0.5:1:600',
       					'RRA:AVERAGE:0.5:6:700',
       					'RRA:AVERAGE:0.5:24:775',
       					'RRA:AVERAGE:0.5:288:797')
			if not os.path.exists('cpu.rrd'):
				# cpu_db
				rrdtool.create('cpu.rrd','--step','300','--start',cur_time,
					'DS:cpu_loadavg_1:GAUGE:600:U:U',
					'DS:cpu_loadavg_5:GAUGE:600:U:U',
					'DS:cpu_loadavg_15:GAUGE:600:U:U',
					'DS:cpu_user:GAUGE:600:U:U',
					'DS:cpu_nice:GAUGE:600:U:U',
					'DS:cpu_system:GAUGE:600:U:U',
					'DS:cpu_iowait:GAUGE:600:U:U',
					'DS:cpu_steal:GAUGE:600:U:U',
					'DS:cpu_idel:GAUGE:600:U:U',
       					'RRA:LAST:0.5:1:600',
       					'RRA:LAST:0.5:6:700',
       					'RRA:LAST:0.5:24:775',
       					'RRA:LAST:0.5:288:797',
       					'RRA:MAX:0.5:1:600',
       					'RRA:MAX:0.5:6:700',
       					'RRA:MAX:0.5:24:775',
       					'RRA:MAX:0.5:288:797',
       					'RRA:MIN:0.5:1:600',
       					'RRA:MIN:0.5:6:700',
       					'RRA:MIN:0.5:24:775',
       					'RRA:MIN:0.5:288:797',
       					'RRA:AVERAGE:0.5:1:600',
       					'RRA:AVERAGE:0.5:6:700',
       					'RRA:AVERAGE:0.5:24:775',
       					'RRA:AVERAGE:0.5:288:797')
			if not os.path.exists('mem.rrd'):
				# mem_db
				rrdtool.create('mem.rrd','--step','300','--start',cur_time,
					'DS:mem_total:GAUGE:600:U:U',
					'DS:mem_freed:GAUGE:600:U:U',
					'DS:mem_used:GAUGE:600:U:U',
					'DS:mem_buffers_freed:GAUGE:600:U:U',
					'DS:mem_buffers_used:GAUGE:600:U:U',
					'DS:mem_used_percent:GAUGE:600:U:U',
					'DS:swap_total:GAUGE:600:U:U',
					'DS:swap_freed:GAUGE:600:U:U',
					'DS:swap_used:GAUGE:600:U:U',
					'DS:swap_used_percnet:GAUGE:600:U:U',
       					'RRA:LAST:0.5:1:600',
       					'RRA:LAST:0.5:6:700',
       					'RRA:LAST:0.5:24:775',
       					'RRA:LAST:0.5:288:797',
       					'RRA:MAX:0.5:1:600',
       					'RRA:MAX:0.5:6:700',
       					'RRA:MAX:0.5:24:775',
       					'RRA:MAX:0.5:288:797',
       					'RRA:MIN:0.5:1:600',
       					'RRA:MIN:0.5:6:700',
       					'RRA:MIN:0.5:24:775',
       					'RRA:MIN:0.5:288:797',
       					'RRA:AVERAGE:0.5:1:600',
       					'RRA:AVERAGE:0.5:6:700',
       					'RRA:AVERAGE:0.5:24:775',
       					'RRA:AVERAGE:0.5:288:797')
			if not os.path.exists('disk.rrd'):
				# disk_db
				rrdtool.create('disk.rrd','--step','300','--start',cur_time,
					'DS:disk_total:GAUGE:600:U:U',
					'DS:disk_freed:GAUGE:600:U:U',
					'DS:disk_used:GAUGE:600:U:U',
					'DS:disk_used_percent:GAUGE:600:U:U',
       					'RRA:LAST:0.5:1:600',
       					'RRA:LAST:0.5:6:700',
       					'RRA:LAST:0.5:24:775',
       					'RRA:LAST:0.5:288:797',
       					'RRA:MAX:0.5:1:600',
       					'RRA:MAX:0.5:6:700',
       					'RRA:MAX:0.5:24:775',
       					'RRA:MAX:0.5:288:797',
       					'RRA:MIN:0.5:1:600',
       					'RRA:MIN:0.5:6:700',
       					'RRA:MIN:0.5:24:775',
       					'RRA:MIN:0.5:288:797',
       					'RRA:AVERAGE:0.5:1:600',
       					'RRA:AVERAGE:0.5:6:700',
       					'RRA:AVERAGE:0.5:24:775',
       					'RRA:AVERAGE:0.5:288:797')
			if not os.path.exists('login_user.rrd'):
				# login_user_db
				rrdtool.create('login_user.rrd','--step','300','--start',cur_time,
					'DS:login_user_num:GAUGE:600:U:U',
       					'RRA:LAST:0.5:1:600',
       					'RRA:LAST:0.5:6:700',
       					'RRA:LAST:0.5:24:775',
       					'RRA:LAST:0.5:288:797',
       					'RRA:MAX:0.5:1:600',
       					'RRA:MAX:0.5:6:700',
       					'RRA:MAX:0.5:24:775',
       					'RRA:MAX:0.5:288:797',
       					'RRA:MIN:0.5:1:600',
       					'RRA:MIN:0.5:6:700',
       					'RRA:MIN:0.5:24:775',
       					'RRA:MIN:0.5:288:797',
       					'RRA:AVERAGE:0.5:1:600',
       					'RRA:AVERAGE:0.5:6:700',
       					'RRA:AVERAGE:0.5:24:775',
       					'RRA:AVERAGE:0.5:288:797')
    def rrdb_update(self):
	"""
	2.插入rrdtool所需的数据
	3.更新rrdtool数据库

	"""
	#sql_cpu = "select Host_ip,Time,Cpu_Utilization from report_list \
	#	where Time > date_format(date_sub(now(),interval 1 HOUR),'%Y-%m-%d %H:00:00') \
	#	and Time< date_format(now(),'%Y-%m-%d %H:00:00')"
	sql_cpu = "select Host_ip,Time,CPU_Loadavg,CPU_User,CPU_Nice,CPU_System,CPU_Iowait,CPU_Steal,CPU_Idel \
		from cpu where Time > date_sub(now(),interval 5 MINUTE) and Time< now()"
	#sql_mem = "select Host_ip,Time,Mem_total,Mem_free,Mem_used,Mem_percent,Swap_total, \
	#	Swap_free,Swap_used,Swap_percent from report_list \
	#	where Time > date_format(date_sub(now(),interval 1 HOUR),'%Y-%m-%d %H:00:00')  \
	#	and Time< date_format(now(),'%Y-%m-%d %H:00:00')"
	sql_mem = "select Host_ip,Time,MEM_Total,MEM_Freed,MEM_Used,MEM_Buffers_Freed,MEM_Buffers_Used,MEM_Used_Percent, \
		SWAP_Total,SWAP_Freed,SWAP_Used,SWAP_Used_Percent from mem \
		where Time > date_sub(now(),interval 5 MINUTE) and Time< now();"
	#sql_disk = "select Host_ip,Time,Disk_total,Disk_free,Disk_used,Disk_percent from report_list \
	#	where Time > date_format(date_sub(now(),interval 1 HOUR),'%Y-%m-%d %H:00:00') \
	#	and Time< date_format(now(),'%Y-%m-%d %H:00:00')"
	sql_disk = "select Host_ip,Time,DISK_Total,DISK_Freed,DISK_Used,DISK_Used_Percent from disk \
		where Time > date_sub(now(),interval 5 MINUTE) and Time< now();"
	#sql_nic = "select Host_ip,Time,Network_traffic_recv,Network_traffic_sent from report_list \
	#	where Time > date_format(date_sub(now(),interval 1 HOUR),'%Y-%m-%d %H:00:00') \
	#	and Time< date_format(now(),'%Y-%m-%d %H:00:00')"
	sql_nic = "select Host_ip,Time,Networktraffic_recv,Networktraffic_recv_err,Networktraffic_sent,Networktraffic_sent_err \
		from network where Time > date_sub(now(),interval 5 MINUTE) and Time< now();"
	#login_user
	sql_login = "select Host_ip,Time,User_num from login_user \
		where Time > date_sub(now(),interval 5 MINUTE) and Time< now();"
	self.cpu_rrd(sql_cpu)
	logging.debug(self.cpu_rrd(sql_cpu))
	self.nic_rrd(sql_nic)
	logging.debug(self.nic_rrd(sql_nic))
	self.mem_rrd(sql_mem)
	logging.debug(self.mem_rrd(sql_mem))
	self.disk_rrd(sql_disk)
	logging.debug(self.disk_rrd(sql_disk))
	self.login_rrd(sql_login)
	logging.debug(self.login_rrd(sql_login))
    #####################cpu###########################################
    def cpu_rrd(self,sql_cpu):
	debug = "This is cpu.rrd to perform the debug result :"
	# mysql configure
	host_sql = self.host
	user = self.user
	password = self.password
	defaultdb = self.defaultdb
	# rrdtool host configure
	host = self.rrdtool_host
	report_dir = self.rrdtool_dir
	#  
	conv = converters.conversions.copy()
	conv[246] = float # convert decimals to floats
	conn = MySQLdb.connect(host_sql,user,password,defaultdb,conv=conv)
	cur = conn.cursor()
	cpu_list = []
	cur.execute(sql_cpu)
	rows = int(cur.rowcount)
	for i in xrange(rows):
		row = cur.fetchone()
		#print row[0],row[1],row[2]
		a = str(row[0])
		l = str(row[1])
		timeArray = time.strptime(l, "%Y-%m-%d %H:%M:%S")
		b = str(int(time.mktime(timeArray)))
		c = row[2].split(',')[0].strip()
		d = row[2].split(',')[1].strip()
		e = row[2].split(',')[2].strip()
		f = str(row[3])
		g = str(row[4])
		h = str(row[5])
		i = str(row[6])
		j = str(row[7])
		k = str(row[8])
		#cpu_list = [a,b,c,d,e,f,g,h,i,j,k]
		#print cpu_list
		for ip in list(host.split(',')):
			#print cpu_list[1],cpu_list[2]
			if ip == a :
			#	print report_dir
				os.chdir(report_dir)
				os.chdir(ip)
			#	print type(cpu_list[1])
			#	print type(cpu_list[2])
				#db = rrdtool.updatev('cpu.rrd','%s:%s:%s:%s:%s:%s:%s:%s:%s:%s' % (b,c,d,e,f,g,h,i,j,k))
				cmd = '/usr/bin/rrdtool updatev cpu.rrd %s:%s:%s:%s:%s:%s:%s:%s:%s:%s' % (b,c,d,e,f,g,h,i,j,k)
				db_update = shell.shell_cmd(cmd)
				print db_update
				time.sleep(1)
				print os.getcwd()
				print "cpu.rrd"
	
	conn.close()
	return (debug+str(db_update))	
    #####################network###########################################
    def nic_rrd(self,sql_nic):
	debug = "This is nic.rrd to perform the debug result :"
	# mysql configure
	host_sql = self.host
	user = self.user
	password = self.password
	defaultdb = self.defaultdb
	# rrdtool host configure
	host = self.rrdtool_host
	report_dir = self.rrdtool_dir
	conv = converters.conversions.copy()
	conv[246] = float # convert decimals to floats
	conn = MySQLdb.connect(host_sql,user,password,defaultdb,conv=conv)
	cur = conn.cursor()
	nic_list = []
	cur.execute(sql_nic)
	rows = int(cur.rowcount)
	for i in xrange(rows):
		row = cur.fetchone()
		a = str(row[0])
		g = str(row[1])
		timeArray = time.strptime(g, "%Y-%m-%d %H:%M:%S")
		b = str(int(time.mktime(timeArray)))
		c = str(row[2])
		d = str(row[4])
		e = str(row[3])
		f = str(row[5])
		# nic_list = [a,b,c,d]
		print "%s %s %s %s %s %s" % (a,b,c,d,e,f)
		for j in list(host.split(',')):
			if j == a:
				os.chdir(report_dir)
				os.chdir(j)
				#print nic_list
				#db = rrdtool.updatev('nic.rrd','%s:%s:%s:%s:%s' % (b,c,d,e,f))
				cmd = '/usr/bin/rrdtool updatev nic.rrd %s:%s:%s:%s:%s' % (b,c,d,e,f)
				db_update = shell.shell_cmd(cmd)
				print db_update
				time.sleep(1)
				print os.getcwd()
				print "nic.rrd"
	conn.close()	
	return (debug+str(db_update))	
    #####################disk###########################################
    def disk_rrd(self,sql_disk):
	debug = "This is disk.rrd to perform the debug result :"
	# mysql configure
	host_sql = self.host
	user = self.user
	password = self.password
	defaultdb = self.defaultdb
	# rrdtool host configure
	host = self.rrdtool_host
	report_dir = self.rrdtool_dir
	conv = converters.conversions.copy()
	conv[246] = float # convert decimals to floats
	conn = MySQLdb.connect(host_sql,user,password,defaultdb,conv=conv)
	cur = conn.cursor()
	disk_list = []
	cur.execute(sql_disk)
	rows = int(cur.rowcount)
	for i in xrange(rows):
		row = cur.fetchone()
		#print row[0],row[1],row[2]
		a = str(row[0])
		g = str(row[1])
		timeArray = time.strptime(g, "%Y-%m-%d %H:%M:%S")
		b = str(int(time.mktime(timeArray)))
		c = str(row[2])
		d = str(row[3])
		e = str(row[4])
		f = str(row[5])
		#disk_list = [a,b,c,d,e,f]
		for j in list(host.split(',')):
			if j == a :
				os.chdir(report_dir)
				os.chdir(j)
				cmd = '/usr/bin/rrdtool updatev disk.rrd %s:%s:%s:%s:%s' % (b,c,d,e,f)
				db_update = shell.shell_cmd(cmd)
				print db_update
				time.sleep(1)
				print os.getcwd()
				print "disk.rrd"
	conn.close()	
	return (debug+str(db_update))	
    #####################mem###########################################
    def mem_rrd(self,sql_mem):
	debug = "This is mem.rrd to perform the debug result :"
	# mysql configure
	host_sql = self.host
	user = self.user
	password = self.password
	defaultdb = self.defaultdb
	# rrdtool host configure
	host = self.rrdtool_host
	report_dir = self.rrdtool_dir
	conv = converters.conversions.copy()
	conv[246] = float # convert decimals to floats
	conn = MySQLdb.connect(host_sql,user,password,defaultdb,conv=conv)
	cur = conn.cursor()
	#mem_list = []
	cur.execute(sql_mem)
	rows = int(cur.rowcount)
	for i in xrange(rows):
		row = cur.fetchone()
		a = str(row[0])
		m = str(row[1])
		timeArray = time.strptime(m, "%Y-%m-%d %H:%M:%S")
		b = str(int(time.mktime(timeArray)))
		c = str(row[2])
		d = str(row[3])
		e = str(row[4])
		f = str(row[5])
		g = str(row[6])
		h = str(row[7])
		i = str(row[8])
		j = str(row[9])
		k = str(row[10])
		l = str(row[11])
		#mem_list = [a,b,c,d,e,f,g,h,k]
		#print "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" %(a,b,c,d,e,f,g,h,i,j,k,l)
		for ip in list(host.split(',')):
			if ip == a :
				#print "%s is %s" %(j,mem_list[0])
				os.chdir(report_dir)
				os.chdir(ip)
				#print os.getcwd()
				cmd = '/usr/bin/rrdtool updatev mem.rrd %s:%s:%s:%s:%s:%s:%s:%s:%s:%s:%s' % (b,c,d,e,f,g,h,i,j,k,l)
				db_update = shell.shell_cmd(cmd)
				print db_update
				time.sleep(1)
				print os.getcwd()
				print "mem.rrd"
	conn.close()	
	return (debug+str(db_update))	

    #####################login_user###########################################
    def login_rrd(self,sql_login):
	debug = "This is login.rrd to perform the debug result :"
	# mysql configure
	host_sql = self.host
	user = self.user
	password = self.password
	defaultdb = self.defaultdb
	# rrdtool host configure
	host = self.rrdtool_host
	report_dir = self.rrdtool_dir
	conv = converters.conversions.copy()
	conv[246] = float # convert decimals to floats
	conn = MySQLdb.connect(host_sql,user,password,defaultdb,conv=conv)
	cur = conn.cursor()
	login_user = []
	cur.execute(sql_login)
	rows = int(cur.rowcount)
	for i in xrange(rows):
		row = cur.fetchone()
		#print row[0],row[1],row[2]
		a = str(row[0])
		e = str(row[1])
		timeArray = time.strptime(e, "%Y-%m-%d %H:%M:%S")
		b = str(int(time.mktime(timeArray)))
		c = str(row[2])
		# login_list = [a,b,c,d]
		for j in list(host.split(',')):
			if j == a:
				os.chdir(report_dir)
				os.chdir(j)
				print row
				cmd = '/usr/bin/rrdtool updatev login_user.rrd %s:%s' % (b,c)
				db_update = shell.shell_cmd(cmd)
				time.sleep(1)
				print db_update
				print os.getcwd()
				print "nic.rrd"
	conn.close()	
	return (debug+str(db_update))	


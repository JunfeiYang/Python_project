#_*_ coding: UTF-8 _*_
import sys,time,os
reload(sys)
sys.setdefaultencoding('utf8')
import rrdtool
import random
import time
import MySQLdb
from otomat.conf import conf
from  otomat.debug  import log as logging

cnf =conf.files_conf_check('/etc/otomat/otomat.cnf')
logfile = cnf.report_log()
logdir = cnf.server_logdir()

if not os.path.exists(logdir):
        os.makedirs(logdir,0o755)

os.chdir(logdir)
logging.set_logger(filename =logfile, mode = 'a')

class graph_rrdtool:
    """
    rrdtool 绘图过程一共有四步：
    1.创建rrdtool数据库
    2.插入rrdtool所需的数据
    3.更新rrdtool数据库
    4.进行rrdtool绘图。
    """
    def __init__(self,filename="/etc/otomat/otomat.cnf",graph=None,title="北京壹號車 系統報告"):
        self.filename = filename
	cnf = conf.files_conf_check(self.filename)
	# rrdtool
	self.rrdtool_cpu = cnf.rrdtool_cpu()
	self.rrdtool_mem = cnf.rrdtool_mem()
	self.rrdtool_disk = cnf.rrdtool_disk()
	self.rrdtool_host = cnf.rrdtool_host()
	self.rrdtool_dir = cnf.rrdtool_dir()
	self.rrdtool_nic = cnf.rrdtool_nic()
	# graph
	self.graph_cpu = cnf.graph_cpu()
	self.graph_mem = cnf.graph_mem()
	self.graph_disk = cnf.graph_disk()
	self.graph_network = cnf.graph_network()
        self.graph = graph
        self.title = title
	# sql
	self.host = cnf.sql_host()
	self.user = cnf.sql_user()
	self.password = cnf.sql_password()
	self.defaultdb = cnf.sql_defaultdb()
        #self.time = str(int(time.time()))
    def rrdb(self):
        """
        1.创建rrdtool的数据库.
        """
        #cur_time = str(int(time.time()))
        cur_time = '1417652469'
	host = self.rrdtool_host
	#print host
	report_dir = self.rrdtool_dir
	#print report_dir
	report_rrd = [self.rrdtool_cpu,self.rrdtool_mem,self.rrdtool_disk,self.rrdtool_nic]
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
        				'DS:input:COUNTER:600:U:U',
        				'DS:output:COUNTER:600:U:U',
       					'RRA:LAST:0.5:1:600',
       					'RRA:LAST:0.5:4:600',
       					'RRA:LAST:0.5:24:600',
       					'RRA:LAST:0.5:288:730',
       					'RRA:MAX:0.5:1:600',
       					'RRA:MAX:0.5:4:600',
       					'RRA:MAX:0.5:24:600',
       					'RRA:MAX:0.5:288:730',
       					'RRA:MIN:0.5:1:600',
       					'RRA:MIN:0.5:4:600',
       					'RRA:MIN:0.5:24:600',
       					'RRA:MIN:0.5:288:730',
       					'RRA:AVERAGE:0.5:1:600',
       					'RRA:AVERAGE:0.5:6:600',
       					'RRA:AVERAGE:0.5:24:600',
       					'RRA:AVERAGE:0.5:288:730')
			if not os.path.exists('cpu.rrd'):
				# cpu_db
				rrdtool.create('cpu.rrd','--step','300','--start',cur_time,
					'DS:cpu_percent:GAUGE:600:U:U',
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
					'DS:mem_free:GAUGE:600:U:U',
					'DS:mem_used:GAUGE:600:U:U',
					'DS:mem_percent:GAUGE:600:U:U',
					'DS:swap_total:GAUGE:600:U:U',
					'DS:swap_free:GAUGE:600:U:U',
					'DS:swap_used:GAUGE:600:U:U',
					'DS:swap_percnet:GAUGE:600:U:U',
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
					'DS:disk_free:GAUGE:600:U:U',
					'DS:disk_used:GAUGE:600:U:U',
					'DS:disk_percnet:GAUGE:600:U:U',
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
	sql_cpu = "select Host_ip,Time,Cpu_Utilization from report_list \
		where Time > date_sub(now(),interval 5 MINUTE) and Time< now()"
	#sql_mem = "select Host_ip,Time,Mem_total,Mem_free,Mem_used,Mem_percent,Swap_total, \
	#	Swap_free,Swap_used,Swap_percent from report_list \
	#	where Time > date_format(date_sub(now(),interval 1 HOUR),'%Y-%m-%d %H:00:00')  \
	#	and Time< date_format(now(),'%Y-%m-%d %H:00:00')"
	sql_mem = "select Host_ip,Time,Mem_total,Mem_free,Mem_used,Mem_percent,Swap_total, \
		Swap_free,Swap_used,Swap_percent from report_list \
		where Time > date_sub(now(),interval 5 MINUTE) and Time< now();"
	#sql_disk = "select Host_ip,Time,Disk_total,Disk_free,Disk_used,Disk_percent from report_list \
	#	where Time > date_format(date_sub(now(),interval 1 HOUR),'%Y-%m-%d %H:00:00') \
	#	and Time< date_format(now(),'%Y-%m-%d %H:00:00')"
	sql_disk = "select Host_ip,Time,Disk_total,Disk_free,Disk_used,Disk_percent from report_list \
		where Time > date_sub(now(),interval 5 MINUTE) and Time< now();"
	#sql_nic = "select Host_ip,Time,Network_traffic_recv,Network_traffic_sent from report_list \
	#	where Time > date_format(date_sub(now(),interval 1 HOUR),'%Y-%m-%d %H:00:00') \
	#	and Time< date_format(now(),'%Y-%m-%d %H:00:00')"
	sql_nic = "select Host_ip,Time,Network_traffic_recv,Network_traffic_sent from report_list \
		where Time > date_sub(now(),interval 5 MINUTE) and Time< now();"
	self.cpu_rrd(sql_cpu)
	logging.debug(self.cpu_rrd(sql_cpu))
	self.nic_rrd(sql_nic)
	logging.debug(self.nic_rrd(sql_nic))
	self.mem_rrd(sql_mem)
	logging.debug(self.mem_rrd(sql_mem))
	self.disk_rrd(sql_disk)
	logging.debug(self.disk_rrd(sql_disk))
    #####################cpu###########################################
    def cpu_rrd(self,sql_cpu):
	# mysql configure
	host_sql = self.host
	user = self.user
	password = self.password
	defaultdb = self.defaultdb
	# rrdtool host configure
	host = self.rrdtool_host
	report_dir = self.rrdtool_dir
	conn = MySQLdb.connect(host_sql,user,password,defaultdb)
	cur = conn.cursor()
	cpu_percent = []
	cur.execute(sql_cpu)
	rows = int(cur.rowcount)
	for i in xrange(rows):
		row = cur.fetchone()
		#print row[0],row[1],row[2]
		a = str(row[0])
		e = str(row[1])
		timeArray = time.strptime(e, "%Y-%m-%d %H:%M:%S")
		b = str(int(time.mktime(timeArray)))
		c = str(row[2])
		cpu_percent = [a,b,c]
		#print cpu_percent[0]
		for j in list(host.split(',')):
			#print cpu_percent[1],cpu_percent[2]
			if j == cpu_percent[0] :
			#	print report_dir
				os.chdir(report_dir)
				os.chdir(j)
			#	print type(cpu_percent[1])
			#	print type(cpu_percent[2])
				db = rrdtool.updatev('cpu.rrd','%s:%s' % (cpu_percent[1],cpu_percent[2]))
				print db
				time.sleep(5)
				print os.getcwd()
				print "cpu.rrd"
    #####################network###########################################
    def nic_rrd(self,sql_nic):
	# mysql configure
	host_sql = self.host
	user = self.user
	password = self.password
	defaultdb = self.defaultdb
	# rrdtool host configure
	host = self.rrdtool_host
	report_dir = self.rrdtool_dir
	conn = MySQLdb.connect(host_sql,user,password,defaultdb)
	cur = conn.cursor()
	nic_list = []
	cur.execute(sql_nic)
	rows = int(cur.rowcount)
	for i in xrange(rows):
		row = cur.fetchone()
		#print row[0],row[1],row[2]
		a = str(row[0])
		e = str(row[1])
		timeArray = time.strptime(e, "%Y-%m-%d %H:%M:%S")
		b = str(int(time.mktime(timeArray)))
		c = str(row[2])
		d = str(row[3])
		nic_list = [a,b,c,d]
		for j in list(host.split(',')):
			if j == nic_list[0] :
				os.chdir(report_dir)
				os.chdir(j)
				print nic_list
				db = rrdtool.updatev('nic.rrd','%s:%s:%s' % (nic_list[1],nic_list[2],
					nic_list[3]))
				time.sleep(1)
				print db
				print os.getcwd()
				print "nic.rrd"

    #####################disk###########################################
    def disk_rrd(self,sql_disk):
	# mysql configure
	host_sql = self.host
	user = self.user
	password = self.password
	defaultdb = self.defaultdb
	# rrdtool host configure
	host = self.rrdtool_host
	report_dir = self.rrdtool_dir
	conn = MySQLdb.connect(host_sql,user,password,defaultdb)
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
		disk_list = [a,b,c,d,e,f]
		for j in list(host.split(',')):
			if j == disk_list[0] :
				os.chdir(report_dir)
				os.chdir(j)
				db = rrdtool.updatev('disk.rrd','%s:%s:%s:%s:%s' % (disk_list[1],
					disk_list[2],disk_list[3],disk_list[4],disk_list[5]))
				print db
				time.sleep(1)
				print os.getcwd()
				print "disk.rrd"
    #####################mem###########################################
    def mem_rrd(self,sql_mem):
	# mysql configure
	host_sql = self.host
	user = self.user
	password = self.password
	defaultdb = self.defaultdb
	# rrdtool host configure
	host = self.rrdtool_host
	report_dir = self.rrdtool_dir
	conn = MySQLdb.connect(host_sql,user,password,defaultdb)
	cur = conn.cursor()
	mem_list = []
	cur.execute(sql_mem)
	rows = int(cur.rowcount)
	for i in xrange(rows):
		row = cur.fetchone()
		#print row[0],row[1],row[2]
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
		k = str(row[8])
		l = str(row[9])
		mem_list = [a,b,c,d,e,f,g,h,k,l]
		#print mem_list
		for j in list(host.split(',')):
			if j == mem_list[0] :
				#print "%s is %s" %(j,mem_list[0])
				os.chdir(report_dir)
				os.chdir(j)
				#print os.getcwd()
				db = rrdtool.updatev('mem.rrd','%s:%s:%s:%s:%s:%s:%s:%s:%s' % (mem_list[1],
					mem_list[2],mem_list[3],mem_list[4],mem_list[5],mem_list[6],
					mem_list[7],mem_list[8],mem_list[9]))
				print db
				time.sleep(1)
				print os.getcwd()
				print "mem.rrd"

    def rrdtool_graph(self):
         rrdtool.graph(self.graph,'--start',self.time,
            '--title',self.title,
            '--vertical-label','bits',
            'DEF:input=rest.rrd:input:LAST',
            'DEF:output=rest.rrd:output:LAST',
            'LINE1:input#0000FF:In traffic',
            'LINE1:output#00FF00:Out traffic\\r',
            'CDEF:bytes_in=input,8,*',
            'CDEF:bytes_out=output,8,*',
            'COMMENT:\\n',
            'GPRINT:bytes_in:LAST:LAST in traffic\: %6.2lf %Sbps',
            'COMMENT:  ',
            'GPRINT:bytes_out:LAST:LAST out traffic\: %6.2lf %Sbps')

def main(argv=sys.argv[1:]):
	t = graph_rrdtool(argv)
	logging.info(("The otomat-report-server has been launched successfully !!!"))
	while True:
		t.rrdb()
		t.rrdb_update()
		time.sleep(300)
		continue
if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))


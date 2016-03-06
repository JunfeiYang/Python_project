#!/usr/bin/python
#_*_ coding:UTF-8 _*_

import sys,os
import threading
import  time,datetime
from logs import log as logging
from plugins import shell
from plugins import env_set
from plugins import config
reload(sys)
sys.setdefaultencoding('utf8')

home_path = os.getcwd()


logfile = 'plat-manager-action.log'
logdir = '/var/log/plat-manager'

if not os.path.exists(logdir):
    os.makedirs(logdir,0o755)
os.chdir(logdir)

logging.set_logger(filename =logfile, mode = 'a')

os.chdir(home_path)

conf = config.tenant_conf('plugins/platform_manager.conf')
########################
# global variable
TENANT_NAME_LIST = conf.tenant_name()
LEN_TENANT_NUM = len(TENANT_NAME_LIST)


def env_set_func(tenant_name):
	# ['kyprivate', 'kycloudprod']
	global TENANT_NAME_LIST 
	rescoure = conf.tenant_rescoure()
	global LEN_TENANT_NUM
	# 10
	len_rescore = len(rescoure)
	for n in range(len(TENANT_NAME_LIST)):
		if tenant_name == TENANT_NAME_LIST[n]:
			suffix = n*5
			url_key = rescoure[suffix][1]
			tenant_id_key = rescoure[suffix+1][1]
			user_name_key = rescoure[suffix+2][1]
			password_key = rescoure[suffix+3][1]
			tenant_name_key = rescoure[suffix+4][1]
			env_dist = {
				#'OS_AUTH_URL':'http://172.16.209.11:5000/v2.0',
				'OS_AUTH_URL':url_key,
				#'OS_TENANT_ID':'f1134680ff48420382bad868071bb115',
				'OS_TENANT_ID':tenant_id_key,
				#'OS_TENANT_NAME':'kycloudprod',
				'OS_TENANT_NAME':tenant_name_key,
				#'OS_USERNAME':'kycloudprod',
				'OS_USERNAME':user_name_key,
				#'OS_PASSWORD':'che001'
				'OS_PASSWORD':password_key
				}	

			keys = env_dist.keys()
			for i in keys:
				value = env_dist[i]
				env_set.set_env(i,value)
			#return os.environ.data
			return env_dist

	

class action_do_work:
	def __init__(self):
		pass
	def tenant_do_work(self,tenant_name,cmd):
		#tenant_name = 'kycloudprod'
		list_dir = '/var/lib/platform-manager/'
		cmd_date = "date  '+%Y-%m-%d'"
		date = shell.shell_cmd(cmd_date)[0].split()[0]
		global list_file
		list_file='list_'+tenant_name+'_'+date
		if not os.path.exists(list_dir):
    			os.makedirs(list_dir,0o755)
			#os.chdir(list_dir)
		#if not os.path.exists(list_file):
			#os.mknod(list_file)
		

		os.chdir(home_path)

		#TENANT_NAME_LIST =
		env_set_func(tenant_name)
		logging.info(os.environ.data)
		##############
		if  os.path.exists(list_file):
			list_file_backup = list_dir+list_file+'.bak'
			backup_cmd = "cp -f %s %s" %(list_dir+list_file,list_file_backup)
			shell.shell_cmd(backup_cmd)
			print "This is backup file" %list_file_backup	
		#####################
		# cmd_floatingip_list 
		######################
		cmd_floatingip_list = "neutron floatingip-list"
		#######################
		# cmd_floatingip_associate
		############################
		floatingip_relation = []
		cmd_fixed = "cat %s|grep -v id |awk '{print $4}'|grep -v ^$" %(list_dir+list_file)
		cmd_float = "cat %s |grep -v id |awk '{print $6}'|grep -v ^$" %(list_dir+list_file)
		cmd_fixed_result = shell.shell_cmd(cmd_fixed)
		cmd_float_result = shell.shell_cmd(cmd_float)
	  
		for n in xrange(len(cmd_fixed_result)):
			p = tuple((cmd_fixed_result[n].split()[0],cmd_float_result[n].split()[0]))
			floatingip_relation.append(p)
		print "This is floatingip_relation: %s" % floatingip_relation 
		#######################################
		fixed = {}
		fixed_keys = []
		fixed_keys_cmd = "neutron floatingip-list |grep -v id|awk '{print $4}'|grep -v ^$"
		fixed_keys_result = shell.shell_cmd(fixed_keys_cmd)
		for fixed_k in xrange(len(fixed_keys_result)):
			fdk = fixed_keys_result[fixed_k].split()[0]
			fixed_keys.append(fdk)
		fixed_value = []
		fixed_value_cmd = "neutron floatingip-list |grep -v id|awk '{print $8}'|grep -v ^$"
		fixed_value_result = shell.shell_cmd(fixed_value_cmd)
		for fixed_v in xrange(len(fixed_value_result)):
			fdv = fixed_value_result[fixed_v].split()[0]
			fixed_value.append(fdv)
		float = {}
		float_keys = []
		float_keys_cmd = "neutron floatingip-list |grep -v id|awk '{print $6}'|grep -v ^$"
		float_keys_result = shell.shell_cmd(float_keys_cmd)
		for float_k in xrange(len(float_keys_result)):
			fok = float_keys_result[float_k].split()[0]
			float_keys.append(fok)
		float_value = []
		float_value_cmd = "neutron floatingip-list |grep -v id|awk '{print $2}'|grep -v ^$"
		float_value_result = shell.shell_cmd(float_value_cmd)
		for float_v in xrange(len(float_value_result)):
			fov = float_value_result[float_v].split()[0]
			float_value.append(fov)
		for n1 in xrange(2):
			fixed[fixed_keys[n1]] = fixed_value[n1] 
		for n2 in xrange(2):
			float[float_keys[n2]] = float_value[n2] 
		######################################
		cmd_floatingip_associate = []
		for f,p in floatingip_relation:
			floatingip = fixed.get(f)
			port = float.get(p)
			cmd_lop = "neutron  floatingip-associate %s %s" % (floatingip,port)
			cmd_floatingip_associate.append(cmd_lop)
		#logging.info("this is floatingip: %s" % floatingip_id)
		#print "this is floatingip_id: %s" % floatingip_id
		#logging.info("this is port_id: %s" % port_id)
		#print "this is port_id: %s" % port_id
		content_list = []
		cmd_name = {
			"list":cmd_floatingip_list,
			"associate":cmd_floatingip_associate
		}
		print cmd_name
		print cmd
		cmd_list = []
		cmd_result = cmd_name.get(cmd)
		if isinstance(cmd_result,str):
			cmd_list.insert(0,cmd_result)
		if isinstance(cmd_result,list):
			cmd_list = cmd_result
		print "This is cmd_list: %s" % cmd_list
		for cmd_l in cmd_list:
			print "this is cmd_l:%s" % cmd_l
			content = shell.shell_cmd(cmd_l)
		#content = os.system('nova list')
			#f = open(list_dir+list_file,'a')
			f = open(list_dir+list_file,'w')
			f.writelines(content)
			f.close()
			logging.info(content)
			content_list.append(content)
			print "This is content: %s" % content
		return content_list
	def thread_do_work(self,tenant_name,cmd):
		threadname = threading.currentThread().getName()
		self.tenant_do_work(tenant_name,cmd)
	def multithread_do_work(self,cmd):
		#global LEN_TENANT_NUM
		global TENANT_NAME_LIST
		#num =  LEN_TENANT_NUM
		threads = []
		for tenant_name in TENANT_NAME_LIST:
			threads.append(threading.Thread(target=self.thread_do_work(tenant_name,cmd),))
		for t in threads:
			t.start()
			time.sleep(0.1)
		for t in threads:
			t.join()
		for item in threading.enumerate():
			print item
		for item in threads:
			print item

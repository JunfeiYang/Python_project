#!/usr/bin/python
#_*_ coding:UTF-8 _*_

import sys,os
import json
import threading
import  time,datetime
from logs import log as logging
from plugins import shell
from plugins import env_set
from plugins import config
reload(sys)
sys.setdefaultencoding('utf8')

home_path = os.getcwd()


logfile = 'plat-check.log'
logdir = '/var/log/plat-manager'

if not os.path.exists(logdir):
        os.makedirs(logdir,0o755)
os.chdir(logdir)
logging.set_logger(filename =logfile, mode = 'a')

os.chdir(home_path)

conf = config.tenant_conf('plugins/platform_check.conf')


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
class action_do_collector:
	def __init__(self):
		pass

	def collector(self,tenant_name):
		#tenant_name = 'kycloudprod'
		list_dir = '/var/lib/platform-check/'
		cmd_date = "date  '+%Y-%m-%d'"
		date = shell.shell_cmd(cmd_date)[0].split()[0]
		check_report_json='check_'+tenant_name+'_'+date+'.json'
		if not os.path.exists(list_dir):
    			os.makedirs(list_dir,0o755)
			#os.chdir(list_dir)
		

		os.chdir(home_path)

		#TENANT_NAME_LIST =
		env_set_func(tenant_name)
		logging.info(os.environ.data)
                #############################
                # collect_id
                ###########################
                collect_id = []
                cmd_id = "nova list |grep -v ^+ |grep -v ID|awk '{print $2}'"
                id_result = shell.shell_cmd(cmd_id)
                for id in xrange(len(id_result)):
                        c_id = id_result[id].split()[0]
                        collect_id.append(c_id)
                #####################################
                #  collect_list 
                ############################
                collect_list = {}
                collect_tenant = tenant_name
                for x in collect_id:
                        ########################
                        # collect_ip
                        ######################
                        cmd_ip = "nova list |grep %s |awk -F',' '{print $1}'|cut -d = -f2" %x
                        ip_result =shell.shell_cmd(cmd_ip)
                        collect_ip = ip_result[0].split()[0]
                        #######################
                        # collect_status
                        #################
                        cmd_status = "nova list |grep %s |awk '{print $6}'" %x
                        status_result = shell.shell_cmd(cmd_status)
                        collect_status = status_result[0].split()[0]
                        #######################
                        # collect_host
                        #######################
                        cmd_host = "nova list |grep %s |awk '{print $4}'" %x
                        host_result = shell.shell_cmd(cmd_host)
                        collect_host = host_result[0].split()[0]
                        #######################
                        # collect_floatingip
                        ####################
                        cmd_floatingip = "nova list |grep %s |awk '{print $13}'" %x
                        floatingip_result = shell.shell_cmd(cmd_floatingip)
                        collect_floatingip = floatingip_result[0].split()[0]
		        #####################
                        # collect_list 
                        ######################
                        collect_list[x] = {
                                        "ip":collect_ip,
                                        "status":collect_status,
                                        "hostname":collect_host,
                                        "tenant":collect_tenant,
                                        "floatingip":collect_floatingip
                        }        
                f = open(list_dir+check_report_json,'w')
                json.dump(collect_list,f)
                f.close()
                logging.info(collect_list)
                #print "This is collect_list:%s" %collect_list
             
	def thread_do_work(self,tenant_name):
		threadname = threading.currentThread().getName()
		self.collector(tenant_name) 
		
	def multithread_do_work(self):
		#global LEN_TENANT_NUM
		global TENANT_NAME_LIST
		#print "This is a tenant_name_list: %s" % TENANT_NAME_LIST
		#num =  LEN_TENANT_NUM
		threads = []
		for tenant_name in TENANT_NAME_LIST:
			threads.append(threading.Thread(target=self.thread_do_work(tenant_name),))
		for t in threads:
			t.setDaemon(1)
		for t in threads:
			t.start()
			time.sleep(0.5)
		for t in threads:
			t.join()
		#for item in threading.enumerate():
		#	#print item
		#	pass
		#for item in threads:
		#	#print item
		#	pass

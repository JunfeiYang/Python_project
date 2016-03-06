#!/usr/bin/python
#_*_ coding:UTF-8 _*_

import sys,os,time
import threading
import collector
from plugins import shell
import json
from logs import log as logging
from plugins import env_set
from plugins import config
reload(sys)
sys.setdefaultencoding('utf8')

home_path = os.getcwd()


logfile = 'platform-check.log'
logdir = '/var/log/plat-manager'

if not os.path.exists(logdir):
        os.makedirs(logdir,0o755)
os.chdir(logdir)
logging.set_logger(filename =logfile, mode = 'a')

os.chdir(home_path)
#########################################################
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


#################################################
def data_process():
        file_list = []
        file_dir = "/var/lib/platform-check/"
        cmd_date = "date  '+%Y-%m-%d'"
        date = shell.shell_cmd(cmd_date)[0].split()[0]
        info = "*"+date+"*"
        #####################
        # file_list
        ######################
        cmd_search = 'find %s -name %s' %(file_dir,info)
        search_result = shell.shell_cmd(cmd_search)
        for x in xrange(len(search_result)):
                se = search_result[x].split()[0]
                file_list.append(se)
        ###################
        # json_list
        ########################
	global json_list
        json_list = []
        for p in file_list:
                fp = json.load(open(p))
                json_list.append(fp)
        #########################
        # platform_info_list
        #########################
        platform_info_list = []
        for j in json_list:
                for n in j.keys():
                        js = j[n]
                        platform_info_list.append(js)
        #print platform_info_list
	logging.info(platform_info_list)
        return platform_info_list               
        
def do_check(ip):
	r"""
	The following code implements these functions.
	ip = 123
	a = {"aa":{"ip":111},"bb":{"ip":222},"cc":{"ip":123}}
	b ={}
	for k,v in a.items():
		if v['ip'] == ip:
			b[str(ip)] = v
	
	b = {"123":{"ip":123}}
	
	"""
	ip_check_list = {}
        #tenant_name = "kyadmin"
        #env_set_func(tenant_name)
<<<<<<< HEAD
	# local openstack platform
        #namespace_id = "qrouter-368182ef-6035-46ae-8910-0b0fc0614478"
	# stating openstack platform
        namespace_id = "qrouter-513b894d-c157-41b9-9bd8-f35ea36114be"
=======
        namespace_id = "qrouter-368182ef-6035-46ae-8910-0b0fc0614478"
>>>>>>> 8c82c008222acb5c9c021e686b59b916124725d1
	cmd_check = "ip netns exec %s fping %s" %(namespace_id,ip)
	p = shell.shell_cmd(cmd_check)[0].split('\n')[0]
	for a in json_list:
		for k,v in a.items():
			if v['ip'] == ip:
				ip_check_list[p] = v
	'''
	f = open('/var/lib/platform-check/instance_check_list','a')
	json.dump(ip_check_list,f)
	f.close()
	'''
	ip_check_list_json = json.dumps(ip_check_list,indent=4)
	print "ip_check_list=",ip_check_list_json 
	#logging.info("ip_check_list=",ip_check_list_json) 
	# print json_list 
	#return ip_check_list
def thread_check(ip):
	thredname = threading.currentThread().getName()
	do_check(ip)
def check_platform():
	collect_results = data_process()
	#print "This is collect_results:%s" %collect_results
	ip_list = []
	for a in collect_results:
		for c,d in a.items():
			if c == 'ip':
				ip_list.append(str(d))
	
        threads = []
	for ip in ip_list:
		threads.append(threading.Thread(target=thread_check(ip),))
	for t in threads:
		t.setDaemon(1)
	for t in threads:
		t.start()
		time.sleep(0.5)
	for t in threads:
		t.join()
        

def main(check):
        if check == "check":
                collect = collector.action_do_collector()
                collect.multithread_do_work()
                print "\033[1;33;40m Executing check procedures .Please wait a monment....\033[0m"
                time.sleep(2)
                check_platform()
        else:
            print "\033[1;33;40m Please use '-h' option.\033[0m"
if __name__ == "__main__":
	from optparse import OptionParser
	parser = OptionParser(version="0.1beta")
	parser.add_option("-c","--check",dest="check",
<<<<<<< HEAD
			 help="Check the platform so the tenant instances,running state.\nThe tool must be run in the network nodes with the namespace.",
=======
			 help="Check the platform so the tenant instances,running state.",
>>>>>>> 8c82c008222acb5c9c021e686b59b916124725d1
			metavar="check")
(options,args) = parser.parse_args()
do = main(options.check)
if len(sys.argv) != 3:
	print "please use the -h or --help"

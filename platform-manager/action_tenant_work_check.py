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
	'''
	　　下面的TENANT_NAME_LIST代表有几个租户，例如：['kyprivate', 'kycloudprod']，
	len(TENANT_NAME_LIST)=2。通过for循环range(2),suffix进行组合，例如：suffix =2*5,
	url_key = rescoure[10][1]取得（http://172.16.209.11:5000/v2.0）
	'''
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
		list_file_nova='list_'+tenant_name+'_'+date
		list_file_volume ='list_'+tenant_name+'_volume'
		list_file_volume_flag =list_file_volume+'_flag'
		list_file_volume_json = list_file_volume+'.json'
		list_file_volume_back = list_file_volume+'.bak'
		if not os.path.exists(list_dir):
    			os.makedirs(list_dir,0o755)
			#os.chdir(list_dir)
		

		os.chdir(home_path)

		#TENANT_NAME_LIST =
		env_set_func(tenant_name)
		logging.info(os.environ.data)
		#####################
		# cmd_list 
		######################
		cmd_list = "nova list"
		#######################
		# cmd_volume_list
		############################
		cmd_volume_list = "nova volume-list"
		######################
		# cmd_stop  
		#######################
		############################
		cmd_stop = []
		if cmd == "stop":
			server_running_id = []
			server_cmd = "nova list |grep Running|awk '{print $2}'"
			cmd_result = shell.shell_cmd(server_cmd)
		#
			for i in xrange(len(cmd_result)):
                		lo = cmd_result[i].split()[0]
                        	server_running_id.append(lo)
		#
		#
			for server_stop in server_running_id:
				cmd_lop = "nova stop %s" %server_stop
				cmd_stop.append(cmd_lop)
			logging.info("this is Server_runing_id: %s" % server_running_id)
			# print "this is Server_runing_id: %s" % server_running_id
		##########################################
		# cmd_start
		#################################
		cmd_start = []
		if cmd == "start":
			server_shutdown_id = []
			server_stop_cmd = " nova list|grep Shutdown |awk '{print $2}'"
			cmd_result_stop = shell.shell_cmd(server_stop_cmd)
		#
			for j in xrange(len(cmd_result_stop)):
				po = cmd_result_stop[j].split()[0]
				server_shutdown_id.append(po)
		
		##
			for server_start in server_shutdown_id:
				cmd_pop = "nova start %s" %server_start
				cmd_start.append(cmd_pop)
		# print "this is Server_shutdown_id: %s" % server_shutdown_id
		####################################
		# cmd_volume_attach
		#######################################
		cmd_volume_attach = []
		if cmd == "volume_attach" :
			start_list = []
			#print "This is json_load:%s" %(list_dir+list_file_volume_json)
			f = open(list_dir+list_file_volume_json)
			json_load =json.load(f,encoding="utf-8")
			f.close()
			print "This is json_load:%s" %json_load
			for j in xrange(len(json_load)):
				cc = json_load[j]
				device = str(cc['device'])
				server_id = str(cc['server_id'])
				volume_id = str(cc['id'])
				ff = tuple((server_id,volume_id,device))
				start_list.append(ff)
			
			for server,volume,device_path in start_list:
				cmd_v = "nova volume-attach %s %s %s" % (server,volume,device_path)
				cmd_volume_attach.append(cmd_v)
			# print "This is server_volume_id: %s" % server_volume_id
			logging.info("This is start_list: %s" % start_list)
		##################################
		# cmd_volume_detach
		###########################
		cmd_volume_detach = []
		if cmd == "volume_detach":
			server_volume_detach_id = []
			volume_detach_id = []
			cmd_detach_server = "nova volume-list |grep in-use|awk '{print $(NF-1)}'"
			cmd_result_server = shell.shell_cmd(cmd_detach_server)
			for de in xrange(len(cmd_result_server)):
				sd = cmd_result_server[de].split()[0]
				server_volume_detach_id.append(sd)
			cmd_detach_volume = "nova volume-list |grep in-use|awk '{print $2}'"
			cmd_result_volume = shell.shell_cmd(cmd_detach_volume)
			for dv in xrange(len(cmd_result_volume)):
				vd = cmd_result_volume[dv].split()[0]
				volume_detach_id.append(vd)
			stop_list = []
			for e in xrange(len(server_volume_detach_id)):
                        	fd = tuple((server_volume_detach_id[e],volume_detach_id[e]))
                        	stop_list.append(fd)
                	for server_volume_01,volume_01 in stop_list:
                        	cmd_d = "nova volume-detach %s %s" % (server_volume_01,volume_01)
                        	cmd_volume_detach.append(cmd_d)
			#print "This is volume_detach_id:%s" % volume_detach_id
			#print "This is server_volume_detach_id:%s" %server_volume_detach_id
		##############################################
		#############################
		# volume_json
		############################
		if cmd == "stop" :
			volume_json_key = []
			#volume_key_cmd = "grep in-use %s |awk '{print $2}'" %(list_dir+list_file_volume)
			volume_key_cmd = "nova volume-list|grep in-use |awk '{print $2}'"
			volume_json_key_result = shell.shell_cmd(volume_key_cmd)
			for k in xrange(len(volume_json_key_result)):
				jk = volume_json_key_result[k].split()[0]
				volume_json_key.append(jk)
			volume_json = []
			for js in xrange(len(volume_json_key)):
				volume_value_cmd = "nova volume-show %s |grep device |awk '{print $4,$5,$6,$7,$12,$13}'" %volume_json_key[js]
				reuslt = shell.shell_cmd(volume_value_cmd)
				reuslt_ev = eval(reuslt[0].split('\n')[0])[0]
				volume_json.append(reuslt_ev)
			# json 
			fp = open(list_dir+list_file_volume_json,'w')
			json.dump(volume_json,fp)
			fp.close()
			logging.info(volume_json)
		
		##############################################
		content_list = []
		cmd_name = {
			"list":cmd_list,
			"stop":cmd_stop,
			"volume_list":cmd_volume_list,
			"start":cmd_start, 
			"volume_attach":cmd_volume_attach,
			"volume_detach":cmd_volume_detach
		}
		print "This is cmdname : %s" % cmd_name
		logging.debug("This is cmd_name:%s" %cmd_name)
		print cmd
		cmd_list = []
		cmd_result = cmd_name.get(cmd)
		if isinstance(cmd_result,str):
			cmd_list.insert(0,cmd_result)
		if isinstance(cmd_result,list):
			cmd_list = cmd_result
		#print "This is cmd_list: %s" % cmd_list
		logging.debug("This is cmd_list: %s" % cmd_list)
		####################
		in_use_check_id = []
		in_use_check_server_cmd = "nova volume-list|grep in-use|awk '{print $(NF-1)}'"
		in_use_check_result = shell.shell_cmd(in_use_check_server_cmd)
		for in_use in xrange(len(in_use_check_result)):
			iu = in_use_check_result[in_use].split()[0]
			in_use_check_id.append(iu)
			 
		for cmd_l in cmd_laist:
			#print "this is cmd_l:%s" % cmd_l
			logging.debug("this is cmd_l:%s" % cmd_l)
			if cmd_l == "nova volume-list":
				content = shell.shell_cmd(cmd_l)
				#content = os.system('nova list')
				back_cmd = "cp -f %s %s" %(list_dir+list_file_volume,list_dir+list_file_volume_back)
				shell.shell_cmd(back_cmd)
				f = open(list_dir+list_file_volume,'w')
				f.writelines(content)
				f.close()
				logging.info(content)
				content_list.append(content)
			else:
				if "nova start" in cmd_l:
					server_id = cmd_l.split()[2] 
					if  server_id in in_use_check_id:  
						content = shell.shell_cmd(cmd_l)
						#content = os.system('nova list')
                                        	f = open(list_dir+list_file_nova,'a')
                                        	f.writelines(content)
                                        	f.close()
                                        	logging.info(content)
                                        	content_list.append(content)

				else:
					content = shell.shell_cmd(cmd_l)
					#content = os.system('nova list')
					f = open(list_dir+list_file_nova,'a')
					f.writelines(content)
					f.close()
					logging.info(content)
					content_list.append(content)
		#print "This is content: %s" % content
		time.sleep(10)
		print "\033[1;31;40m Tenant: %s perform the %s action ,please later.....\033[0m" % (tenant_name,cmd)
		##############################
		# check_result_instance and check_result_volume
		##################################
		# check_result_instance
		cmd_check = "nova list |awk '{print $6}'|grep -v Status|grep -v ^$"
		check_cmd_result = shell.shell_cmd(cmd_check)
		check_result = []
		for c in xrange(len(check_cmd_result)):
			check = check_cmd_result[c].split()[0]
			check_result.append(check)
		num = len(check_result)
		###########################3
		# check_result_volume
		cmd_check_volume = "nova volume-list|grep -v Status|awk '{print $4}'|grep -v ^$"
		check_volume_result = shell.shell_cmd(cmd_check)
		check_volume_result = []
		for v in xrange(len(check_volume_result)):
			check_v = check_cmd_result[v].split()[0]
			check_volume_result.append(check_v)
		num_volume = len(check_volume_result)
		#print "I'am herer"
		if cmd == "stop" or cmd == "volume_detach":
			if num == check_result.count("SHUTOFF") and num_volume == check_volume_result.count("available"):
				logging.info("%s %s" %(check_result,check_volume_result))
				logging.info("Tenant: %s All instance stop successfully!" %tenant_name)
				logging.info("Tenant: %s All volume deattch successfully!" %tenant_name)
				print "\033[1;31;40m Tenant: %s all instance stop successfully!\033[0m" % tenant_name
				print "\033[1;31;40m Tenant: %s all volume deattch successfully!\033[0m" % tenant_name
			elif num == check_result.count("SHUTOFF"):
				logging.info(check_result)
				logging.info("Tenant: %s All instance stop successfully!" %tenant_name)
				print "\033[1;31;40m Tenant: %s all instance stop successfully!\033[0m" % tenant_name
			elif 0 == check_result.count("SHUTOFF"):
				logging.info(check_result)
				logging.critical("Tenant: %s All instance stop failure!" %tenant_name)
			elif num != check_result.count("SHUTOFF"):
				logging.info(check_result)
				logging.error("Tenant:%s All your stoped operating withou success!" %tenant_name)
			elif num_volume == check_volume_result.count("available"):
				logging.info(check_volume_result)
				logging.info("Tenant: %s All volume deattch successfully!" %tenant_name)
				print "\033[1;31;40m Tenant: %s all volume deattch successfully!\033[0m" % tenant_name
			elif 0 == check_volume_result.count("available"):
				logging.info(check_volume_result)
				logging.critical("Tenant: %s All volume deattch failure!" %tenant_name)
			elif num != check_result.count("SHUTOFF") or num_volume != check_volume_result.count("available"):
				logging.info("There are info %s,%s" %(check_volume_result,check_result))
				logging.error("Tenant:%s All your stoped operating withou success!" %tenant_name)
		if cmd == "start":
			#######################################
			if num == check_result.count("ACTIVE"):
				logging.info(check_result)
				logging.info("Tenant:%s All instance started successfully!" %tenant_name)
				print "\033[1;31;40m Tenant:%s All instance started successfully!\033[0m" %tenant_name
			elif 0 == check_result.count("ACTIVE"):
				logging.info(check_result)
				logging.critical("Tenant: %s All instance start failure!" %tenant_name)
			elif num != check_result.count("ACTIVE"):
				logging.info(check_result)
				logging.error("Tenant:%s All your started operating withou success!" %tenant_name)
		if cmd == "volume_attach":
			check_volume_name_old = []
			cmd_volume_name_old ="grep  in-use %s |awk '{print $2}'" %(list_file_volume)
			name_old_result = shell.shell_cmd(cmd_volume_name_old)
			for o in xrange(len(name_old_result)):
				vo = name_old_result[o].split()[0]
				check_volume_name_old.append(vo)
			check_volume_name = []
			cmd_volume_name ="nova volume-list |grep in-use|awk '{print $2}'"
			name_result = shell.shell_cmd(cmd_volume_name)
			for l in xrange(len(name_result)):
				vl =  name_result[l].split()[0]
				check_volume_name.append(vl)
			#######################################
			if len(check_volume_name) == len(check_volume_name_old):
				logging.info((check_volume_result))
				logging.info("Tenant:%s All volume attach successfully!" %tenant_name)
				print "\033[1;31;40m Tenant:%s All volume attach successfully!\033[0m" %tenant_name
				flag = open(list_dir+list_file_volume_flag,'w')
				flag.writelines('0')
				flag.close()
				return 0
			elif len(check_volume_name) == 0:
				logging.info(check_volume_result)
				logging.critical("Tenant: %s All volume attach failure!" %tenant_name)
				flag = open(list_dir+list_file_volume_flag,'w')
				flag.writelines('1')
				flag.close()
				return 1
			else:
				logging.info(check_volume_result)
				logging.error("Tenant:%s All your started operating withou success!" %tenant_name)
				flag = open(list_dir+list_file_volume_flag,'w')
				flag.writelines('-1')
				flag.close()
				return -1
		
	def thread_do_work(self,tenant_name,cmd):
		threadname = threading.currentThread().getName()
		self.tenant_do_work(tenant_name,cmd) 
		
	def multithread_do_work(self,cmd):
		#global LEN_TENANT_NUM
		global TENANT_NAME_LIST
		#print "This is a tenant_name_list: %s" % TENANT_NAME_LIST
		#num =  LEN_TENANT_NUM
		threads = []
		for tenant_name in TENANT_NAME_LIST:
			threads.append(threading.Thread(target=self.thread_do_work(tenant_name,cmd),))
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

#!/usr/bin/python
#_*_ coding:UTF-8 _*_

import sys,os,time
import action_tenant_work as action
from logs import log as logging
reload(sys)
sys.setdefaultencoding('utf8')

home_path = os.getcwd()


logfile = 'platform-manager.log'
logdir = '/var/log/plat-manager'

if not os.path.exists(logdir):
    os.makedirs(logdir,0o755)
os.chdir(logdir)
logging.set_logger(filename =logfile, mode = 'a')

os.chdir(home_path)

<<<<<<< HEAD
######
# Global variable
cmd_list = 'list'
cmd_volume_list = 'volume_list'


def shutdown_instance():
	global cmd_list
=======

def shutdown_instance():
	global cmd_list
	cmd_list = 'list'
>>>>>>> 8c82c008222acb5c9c021e686b59b916124725d1
	cmd_stop = 'stop'
	cmd = [cmd_list,cmd_stop]
	#cmd = [cmd_list]
	for i in cmd:
		do = action.action_do_work()
		do.multithread_do_work(i)
<<<<<<< HEAD
		print "########cmd_stop:%s" %i

def volume_detach():
	global cmd_volume_list
	cmd_volume_detach = 'volume_detach'
	cmd = [cmd_volume_list,cmd_volume_detach]
	#cmd = [cmd_volume_detach]
	for j in cmd:
		do = action.action_do_work()
		do.multithread_do_work(j)
		print "########cmd_volume_detach:%s" %j
=======

def volume_detach():
	global cmd_volume_list
	cmd_volume_list = 'volume_list'
	cmd_volume_detach = 'volume_detach'
	cmd = [cmd_volume_list,cmd_volume_detach]
	#cmd = [cmd_volume_list]
	for j in cmd:
		do = action.action_do_work()
		do.multithread_do_work(j)
>>>>>>> 8c82c008222acb5c9c021e686b59b916124725d1
	
	

def startup_instance():
<<<<<<< HEAD
        #global cmd_list
	cmd_start = 'start'
	#cmd = [cmd_list,cmd_start]
	cmd = [cmd_start]
	for x in cmd:
		do = action.action_do_work()
		do.multithread_do_work(x)
		print "########cmd_start:%s" %x

def volume_attach():
	#global cmd_volume_list
	cmd_volume_attach = 'volume_attach'
	#cmd = [cmd_volume_list,cmd_volume_attach]
	cmd = [cmd_volume_attach]
	for y in cmd:
		do = action.action_do_work()
		do.multithread_do_work(y)
		print "########cmd_volume_attach:%s" %y
=======
	cmd_list= 'list'
	cmd_start = 'start'
	cmd = [cmd_list,cmd_start]
	for x in cmd:
		do = action.action_do_work()
		do.multithread_do_work(x)

def volume_attach():
	global cmd_volume_list
	cmd_volume_list = 'volume_list'
	cmd_volume_attach = 'volume_attach'
	cmd = [cmd_volume_list,cmd_volume_attach]
	for y in cmd:
		do = action.action_do_work()
		do.multithread_do_work(y)
>>>>>>> 8c82c008222acb5c9c021e686b59b916124725d1
def do_work(action):
	if action == 'stop':
		shutdown_instance()
		#time.sleep(10)
		volume_detach()
	elif action == 'start':
		volume_attach()
		#time.sleep(10)
		startup_instance()

if __name__ == "__main__":
	from optparse import OptionParser
<<<<<<< HEAD
	parser = OptionParser(version="0.2beta")
=======
	parser = OptionParser(version="0.1beta")
>>>>>>> 8c82c008222acb5c9c021e686b59b916124725d1
	parser.add_option("-a","--action",dest="action",
			 help="Stop or start virtual machine and mount cloud devices.",
			metavar="start|stop")
(options,args) = parser.parse_args()
do = do_work(options.action)
if len(sys.argv) != 3:
<<<<<<< HEAD
	print "\033[1;33;40m please use the -h or --help \33[0m"
=======
	print "please use the -h or --help"
>>>>>>> 8c82c008222acb5c9c021e686b59b916124725d1

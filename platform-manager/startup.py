#!/usr/bin/python
#_*_ coding:UTF-8 _*_

import sys,os
import threading
import  Queue
from logs import log as logging
from plugins import shell
from plugins import env_set
from plugins import config
reload(sys)
sys.setdefaultencoding('utf8')


logfile = 'plat-manager-startup.log'
logdir = '/var/plat-manager'

if not os.path.exists(logdir):
    os.makedirs(logdir,0o755)
os.chdir(logdir)
logging.set_logger(filename =logfile, mode = 'a')


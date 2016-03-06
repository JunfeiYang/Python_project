#!/usr/bin/env python
import sys
import os
import traceback
import re

argv = sys.argv
argn = len(argv)
if argn == 1:
  config_module = "config"
elif argn == 2:
  config_module = argv[1].split(".")
  if len(config_module) > 2:
    print "Usage: python %s [config_module]"%argv[0]
    print "config_module must like that 'XXX.py' or 'XXX'"
    sys.exit(0)
  config_module = config_module[0]
else:
  print "Usage: python %s [config_module]"%argv[0]
  sys.exit(0)

print "load config module: " + config_module

for key, val in vars(__import__(config_module)).iteritems():
  if key.startswith('__') and key.endswith('__'):
    continue
  vars()[key] = val

from BitsflowTest import *

script = u'''#!/bin/sh

export RELEASE_HOME=%s
export YOYO_LOG_DIR=%s

ulimit -c unlimited
ulimit -n 102400
. $RELEASE_HOME/bf_setenv.sh
export YOYO_DEFAULT_LOG_LVL=Debug
export YOYO_LOG_CORE_DHT=Debug
export YOYO_LOG_DATACELL_GENERAL=Debug
export YOYO_LOG_DATACELL_BACKEND=Debug
export YOYO_LOG_DATACELL_DAEMON=Debug
export YOYO_LOG_DATACELL_API=Debug
export YOYO_LOG_CORE_FILE=Debug
export YOYO_LOG_DATACELL_TIME_SERIES_BACKEND=Debug
export YOYO_LOG_DATACELL_FILE_SYSTEM_BACKEND=Debug
#export YOYO_DEFAULT_LOG_LVL=%s
export YOYO_LOG_ROTATION_LINES=104857600
export YOYO_LOG_ROTATION_FILES=5
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$RELEASE_HOME/lib:/usr/lib:/usr/local/lib

'''

run = u'''$RELEASE_HOME/bin/DataCell -d -logfile $YOYO_LOG_DIR/%s -cfgfile $RELEASE_HOME/conf/%s -pidfile $YOYO_LOG_DIR/%s'''
run_with_fiu = u'''fiu-run -x $RELEASE_HOME/bin/DataCell -logfile $YOYO_LOG_DIR/%s -cfgfile $RELEASE_HOME/conf/%s -pidfile $YOYO_LOG_DIR/%s'''

class DataCellTest(BitsflowTest):
  intro =  "Welcome to yoyo-shell, please use 'help' to show all commands!\n\n"
  intro += "Follow me to install DataCell:\n"
  intro += "  1) prepare yoyopkg-xxx-noarch.tar.gz\n"
  intro += "  2) run 'installYoyopkg /yoyopkg_path/yoyopkg-xxx-noarch.tar.gz'\n"
  intro += "  3) run 'yoyopkg install --tag DATACELL_BLEEDING_EDGE'\n"
  intro += "  4) prepare agent.xml.sample, groupd.xml.sample and yoyo.lic in current path\n"
  intro += "  5) run 'configBitsflow agent.xml.sample yoyo.lic'\n"
  intro += "  6) run 'configGroupd groupd.xml.sample'\n"
  intro += "  7) run 'startAgent'\n"
  intro += "  8) run 'startGroupd'\n"
  intro += "  9) prepare DataCell.xml.sample in current path\n"
  intro += " 10) run 'configDataCell DataCell.xml.sample'\n"
  intro += " 11) run 'startDataCell'\n"
  intro += " 12) run 'ps' (show DataCell process)\n"
  intro += " 13) run 'getBitsflowLog' (download Bitsflow logs from all nodes)\n"
  intro += " 14) run 'getDataCellLog' (download DataCell logs from all nodes)\n"

  def __init__(self):
    BitsflowTest.__init__(self)

  def getDataCellLog(self, pc):
    print "\n====== IP: " + pc + " getDataCellLog ======"
    tarFolder = "DataCellLog-"+pc 
    tarLogCmd = "rm -rf DataCellLog*;mkdir %s;cd %s;gdb --pid=`cat %s` --command=~/yoyo_gdb_attach | tee datacell.stack;cp -rf %s %s %s ./;cd ~;tar cvzf DataCellLog.tar.gz %s" %(tarFolder, tarFolder, os.path.join(datacell_log_home, datacell_pid_name), os.path.join(datacell_log_home, "%s*"%datacell_log_name), os.path.join(datacell_storage_home,"*core*"), os.path.join(release_home, "conf", datacell_conf_name), tarFolder)
    self.singleExecute(pc, tarLogCmd)
 
  def do_getDataCellLog(self, user_input):
    """Download datacell logs"""
    try:
      self.startWork(self.getDataCellLog, datacell_list)
      self.getFile("DataCellLog.tar.gz", None, datacell_list)
    except:
      print sys.exc_info()
    finally:
      pass 

  def do_backupDataCellVolume(self, user_input):
    """Usage: backupDataCellVolume dir"""
    if len(user_input) == 0:
      print "Usage: backupDataCellVolume dir"
    else:
      cmd = "mkdir %s;mv  %s %s;"%(user_input,os.path.join(datacell_storage_home),user_input)
      self.parallelExecute(cmd, datacell_list)
      for volume in datacell_volumes:
         cmd = "mv %s %s;"%(volume, user_input)
         cmd += "mkdir %s;"%(volume)
         self.parallelExecute(cmd, datacell_list)

  def do_backupDataCellLog(self, user_input):
     """Usage: backupDataCellLog dir"""
     if len(user_input) == 0:
       print "Usage: backupDataCellLog dir"
     else:
       cmd = "tar -jcf  %s.tar.bz2  %s ; tar -jcf  core.tar.bz2  %s ;"%(os.path.join(datacell_log_home, "%s"%datacell_log_name),os.path.join(datacell_log_home, "%s*"%datacell_log_name), os.path.join(datacell_storage_home,"*core*"));
       cmd += "mkdir %s; mv %s.tar.bz2 %s; mv  core.tar.bz2 %s; %s > %s;"%(user_input, os.path.join(datacell_log_home, "%s"%datacell_log_name), user_input, user_input, self.createYoyopkgCmd("ls"), os.path.join(user_input, "version"))
       cmd += "cd %s;source bf_setenv.sh;cd;%s/bin/agent_stats -agent localhost:%s > %s" %(release_home, release_home, agent_port, os.path.join(user_input, "agent_stats.out"))
       self.parallelExecute(cmd, datacell_list)

  def do_diskFailed(self, user_input):
    """make write/read system call failed at [ip1 ip2 ... ipN] randomly"""
    if len(user_input) == 0:
      print "Usage: diskFailed [ip1 ip2 ... ipN]"
    else:
      inputs = user_input.split()
      cmd = "fiu-ctrl -c 'enable_random name=posix/io/*,probability=0.25' `cat %s`"%os.path.join(datacell_log_home, datacell_pid_name)
      self.serialExecute(cmd, inputs) 

  def do_memoryFailed(self, user_input):
    """make malloc system call failed at [ip1 ip2 ... ipN] randomly"""
    if len(user_input) == 0:
      print "Usage: memoryFailed [ip1 ip2 ... ipN]"
    else:
      inputs = user_input.split()
      cmd = "fiu-ctrl -c 'enable_random name=libc/mm/*,probability=0.05' `cat %s`"%os.path.join(datacell_log_home, datacell_pid_name)
      self.serialExecute(cmd, inputs)

  def do_disableDiskFailed(self, user_input):
    """disable write/read system call failed at [ip1 ip2 ... ipN]"""
    if len(user_input) == 0:
      print "Usage: disableDiskFailed [ip1 ip2 ... ipN]"
    else:
      inputs = user_input.split()
      cmd = "fiu-ctrl -c 'disable name=posix/io/*' `cat %s`"%os.path.join(datacell_log_home, datacell_pid_name)
      self.serialExecute(cmd, inputs)

  def do_disableMemoryFailed(self, user_input):
    """disable malloc system call failed at [ip1 ip2 ... ipN]"""
    if len(user_input) == 0:
      print "Usage: disableMemoryFailed [ip1 ip2 ... ipN]"
    else:
      inputs = user_input.split()
      cmd = "fiu-ctrl -c 'disable name=libc/mm/*' `cat %s`"%os.path.join(datacell_log_home, datacell_pid_name)
      self.serialExecute(cmd, inputs)


  def do_startDataCell(self, user_input):
    """start DataCell at [ip1 ip2 ... ipN]"""
    if len(user_input) == 0:
      self.parallelExecute("sh %s"%os.path.join(release_home, "runDataCell.sh"), datacell_list)
    else:
      inputs = user_input.split()
      self.parallelExecute("sh %s"%os.path.join(release_home, "runDataCell.sh"), inputs)

  def do_startDataCellWithFiu(self, user_input):
    """start DataCell with Fiu at [ip1 ip2 ... ipN]"""
    if len(user_input) == 0:
      self.parallelExecute("sh %s"%os.path.join(release_home, "runDataCellWithFiu.sh"), datacell_list)
    else:
      inputs = user_input.split()
      self.parallelExecute("sh %s"%os.path.join(release_home, "runDataCellWithFiu.sh"), inputs)


  def do_rmDataCellStorage(self, user_input):
    """Remove all files which under the datacell_storage_home and all logs"""
    self.parallelExecute("rm -rf %s %s"%(os.path.join(datacell_log_home, "%s*"%datacell_log_name), os.path.join(datacell_storage_home, "*core*")), datacell_list)
    self.parallelExecute("rm -rf %s/*"%(datacell_storage_home), datacell_list)
    for volume in datacell_volumes:
      self.parallelExecute("rm -rf %s/*"%(volume), datacell_list)


  def do_rmDataCellLog(self, user_input):
    """Remove datacell logs"""
    self.parallelExecute("rm -rf %s %s"%(os.path.join(datacell_log_home, "%s*"%datacell_log_name), os.path.join(datacell_storage_home,"*core*")), datacell_list)

  def do_stopDataCell(self, user_input):
    """kill DataCell [ip1 ip2 ... ipN]"""
    if len(user_input) == 0:
      self.parallelExecute("kill `cat %s`"%os.path.join(datacell_log_home, datacell_pid_name), datacell_list)
    else:
      inputs = user_input.split()
      self.parallelExecute("kill `cat %s`"%os.path.join(datacell_log_home, datacell_pid_name), inputs)

  def do_killDataCell(self, user_input):
    """kill -9 DataCell [ip1 ip2 ... ipN]"""
    if len(user_input) == 0:
      self.parallelExecute("kill -9 `cat %s`"%os.path.join(datacell_log_home, datacell_pid_name), datacell_list)
    else:
      inputs = user_input.split()
      self.parallelExecute("kill -9 `cat %s`"%os.path.join(datacell_log_home, datacell_pid_name), inputs)

  def do_ps(self, user_input):
    """Usage: ps [processName] (If no processName, we'll "ps DataCell")"""
    if len(user_input) == 0:
      cmd = "ps aux|grep %s/bin/DataCell"%release_home
    else:
      cmd = "ps aux|grep %s"%user_input
    self.serialExecute(cmd)

  def do_checkBootstrap(self, user_input):
    " Usage : find datacell Stroage Bootstrap Finished"
    if len(user_input) == 0:
      cmd = """grep -R "Storage Bootstrap Finished" %s""" %(os.path.join(datacell_log_home, datacell_log_name))
    else:
      cmd = """grep -R "%s"  %s""" %(user_input,os.path.join(datacell_log_home, datacell_log_name))
    self.serialExecute(cmd)

  def do_checkCoreFile(self, user_input):
    " Usage : check core file"
    if len(user_input) == 0:
      cmd = "ls -la  %s" %(os.path.join(datacell_storage_home))
    else:
      cmd = """ls -la "%s" """ %(os.path.join(user_input))
    self.serialExecute(cmd)

  def do_du(self, user_input):
    " Usage : check core file"
    if len(user_input) == 0:
        cmd = "du -sh %s " %(" ".join(datacell_volumes))
    else:
        cmd = "du %s %s " %(user_input, " ".join(datacell_volumes))
    self.serialExecute(cmd)

  def createRunScript(self):
    f = open("runDataCell.sh", "w")
    runScript = script + run
    runScript = runScript%(release_home, datacell_log_home, datacell_log_level, datacell_log_name, datacell_conf_name, datacell_pid_name)
    f.write(runScript)
    f.close()

    f = open("runDataCellWithFiu.sh", "w")
    runScript = script + run_with_fiu
    runScript = runScript%(release_home, datacell_log_home, datacell_log_level, datacell_log_name, datacell_conf_name, datacell_pid_name)
    f.write(runScript)
    f.close()


  def do_configDataCell(self, user_input):
    """Usage: configDataCell DataCell.xml.sample"""
    inputs = user_input.split()
    inputs_len = len(inputs)

    if inputs_len != 1:
      print "Usage: configDataCell DataCell.xml.sample"
      return
    else:
      try:
        self.createGDBScript()
        self.putFile("yoyo_gdb_attach")
        self.createRunScript()
        self.putFile("runDataCell.sh", os.path.join(release_home, "runDataCell.sh"))
        self.putFile("runDataCellWithFiu.sh", os.path.join(release_home, "runDataCellWithFiu.sh"))

        confPath  = os.path.join(release_home, "conf")
        self.parallelExecute("mkdir -p %s %s %s"%(confPath, datacell_storage_home, datacell_log_home), datacell_list)
        remoteDCConf = os.path.join(confPath, datacell_conf_name)
        for ip in datacell_list:
          localDCConf = "%s.%s"%(datacell_conf_name, ip)
          os.system("cp %s %s"%(inputs[0], localDCConf))
          replace = "sed -i 's/<Name>DC_NODE_1<\/Name>/<Name>%s<\/Name>/g' %s"%(ip, localDCConf)
          os.system(replace)
          replace = "sed -i 's/<Root>.*<\/Root>/<Root>%s<\/Root>/g' %s"%(re.escape(datacell_storage_home), localDCConf)
          os.system(replace)
          replace = "sed -i 's/<Agent>.*<\/Agent>/<Agent>localhost:%s<\/Agent>/g' %s"%(agent_port, localDCConf)
          os.system(replace)
          self.putFileToPC(localDCConf, remoteDCConf, ip)
      except:
        traceback.print_exc()


if __name__ == "__main__":
  datacellctl = DataCellTest()
  datacellctl.cmdloop()

#!/usr/bin/env python
from config import *
from BitsflowTest import *
from NetVMUtil import *
import sys
import os
import traceback
import re

workflow_home=os.path.join(release_home, "modules/workflow")
workflow_conf_name=os.path.join(workflow_home, "conf/workflow.xml")
workflow_log_name=os.path.join(workflow_home, "logs/workflow.log*")
workflow_pid_name=os.path.join(workflow_home, "logs/workflow.pid")
workflow_db_name=os.path.join(workflow_home, "*.db")

dsched_home=os.path.join(release_home, "modules/dsched")
dsched_conf_name=os.path.join(dsched_home, "conf/dsched.xml")
dsched_log_name=os.path.join(dsched_home, "logs/dsched.log*")
dsched_pid_name=os.path.join(dsched_home, "logs/dsched.pid")
dsched_db_name=os.path.join(dsched_home, "*.db")

class NetVMTest(BitsflowTest, NetVMUtil):
  intro =  "Welcome to yoyo-shell, please use 'help' to show all commands!\n\n"
  intro += "Follow me to install NetVM:\n"
  intro += "  1) prepare yoyopkg-xxx-noarch.tar.gz\n"
  intro += "  2) run 'installYoyopkg /yoyopkg_path/yoyopkg-xxx-noarch.tar.gz'\n"
  intro += "  3) run 'yoyopkg install --tag WORKFLOW_BLEEDING_EDGE'\n"
  intro += "  4) prepare agent.xml.sample, groupd.xml.sample and yoyo.lic in current path\n"
  intro += "  5) run 'configBitsflow agent.xml.sample yoyo.lic'\n"
  intro += "  6) run 'configGroupd groupd.xml.sample'\n"
  intro += "  7) run 'startAgent'\n"
  intro += "  8) run 'startGroupd'\n"
  intro += "  9) run 'yoyopkg install workflow_conf_default-1.0.4'\n"
  intro += "  10) run 'startWorkflow'\n"
  intro += "  11) run 'yoyopkg install dsched_conf_default-1.0.1'\n"
  intro += "  11) run 'startDsched'\n"

  def __init__(self, bitsflowHome, pcList, username, password):
    BitsflowTest.__init__(self)
    NetVMUtil.__init__(self)

  def getWorkflowLog(self, pc):
    print "\n====== IP: " + pc + " getWorkflowLog ======"
    tarFolder = "WorkflowLog-"+pc 
    tarLogCmd = "rm -rf WorkflowLog*;mkdir %s;cd %s;gdb --pid=`cat %s` --command=~/yoyo_gdb_attach | tee workflow.stack;cp -rf %s %s %s %s ./;cd ~;tar cvzf WorkflowLog.tar.gz %s" %(tarFolder, tarFolder, workflow_pid_name, workflow_log_name, os.path.join(workflow_home,"*core*"), workflow_conf_name, workflow_db_name, tarFolder)

    self.singleExecute(pc, tarLogCmd)

  def do_getWorkflowLog(self, user_input):
    try:
      self.startWork(self.getWorkflowLog, workflow_list)
      self.getFile("WorkflowLog.tar.gz", None, dsched_list)
    except:
      print sys.exc_info()
    finally:
      pass


  def getDschedLog(self, pc):
    print "\n====== IP: " + pc + " getDschedLog ======"
    tarFolder = "DschedLog-"+pc 
    tarLogCmd = "rm -rf DschedLog*;mkdir %s;cd %s;gdb --pid=`cat %s` --command=~/yoyo_gdb_attach | tee dsched.stack;cp -rf %s %s %s %s ./;cd ~;tar cvzf DschedLog.tar.gz %s" %(tarFolder, tarFolder, dsched_pid_name, dsched_log_name, os.path.join(dsched_home,"*core*"), dsched_conf_name, dsched_db_name, tarFolder)

    self.singleExecute(pc, tarLogCmd)

  def do_getDschedLog(self, user_input):
    try:
      self.startWork(self.getDschedLog, dsched_list)
      self.getFile("DschedLog.tar.gz", None, dsched_list)
    except:
      print sys.exc_info()
    finally:
      pass

  def do_ps(self, user_input):
    """Usage: ps [processName] (If no processName, we'll "ps netvm")"""
    if len(user_input) == 0:
      cmd = "ps aux|grep netvm"
    else:
      cmd = "ps aux|grep %s"%user_input
    self.serialExecute(cmd)

  def do_rmWorkflowLog(self, user_input):
    self.parallelExecute("rm -rf %s"%(os.path.join(release_home, "modules/workflow/logs/*log*")))

  def do_rmWorkflowStorage(self, user_input):
    self.parallelExecute("rm -rf %s"%(os.path.join(release_home, "modules/workflow/logs/*log*")), workflow_list)
    self.parallelExecute("rm -rf %s"%(os.path.join(release_home, "modules/workflow/*.log*")), workflow_list)
    self.parallelExecute("rm -rf %s"%(os.path.join(release_home, "modules/workflow/core*")), workflow_list)
    self.parallelExecute("rm -rf %s"%(os.path.join(release_home, "modules/workflow/*.db")), workflow_list)

  def do_startWorkflow(self, user_input):
    self.doyoyopkg("start workflow", workflow_list)

  def do_stopWorkflow(self, user_input):
    self.doyoyopkg("stop workflow", workflow_list)

  def do_checkWorkflow(self, user_input):
    self.doyoyopkg("interrogate workflow", workflow_list)


  def do_rmDschedLog(self, user_input):
    self.parallelExecute("rm -rf %s"%(os.path.join(release_home, "modules/dsched/logs/*log*")), dsched_list)

  def do_rmDschedStorage(self, user_input):
    self.parallelExecute("rm -rf %s"%(os.path.join(release_home, "modules/dsched/logs/*log*")), dsched_list)
    self.parallelExecute("rm -rf %s"%(os.path.join(release_home, "modules/dsched/*.log*")), dsched_list)
    self.parallelExecute("rm -rf %s"%(os.path.join(release_home, "modules/dsched/core*")), dsched_list)
    self.parallelExecute("rm -rf %s"%(os.path.join(release_home, "modules/dsched/*.db")), dsched_list)

  def do_startDsched(self, user_input):
    self.doyoyopkg("start dsched", dsched_list)

  def do_stopDsched(self, user_input):
    self.doyoyopkg("stop dsched", dsched_list)

  def do_checkDsched(self, user_input):
    self.doyoyopkg("interrogate dsched", dsched_list)

  def do_batchCmd(self, user_input):
    """Usage: batchCmd batch_file
    Run batch cmds, file example:

    # Terminage all jobs
    self.do_dsTerminateAllJobs("")

    # Clear exited jobs
    self.do_dsClearExitedJobs("")

    """
    if len(user_input) < 1:
      print "Usage: batchCmd batch_file"

    if os.path.isfile(user_input):
      try:
        dir_name = os.path.dirname(user_input)
        if dir_name not in sys.path:
          sys.path.append(dir_name)
        exec(open(user_input))
      except Exception, e:
        print "error:", e
    else:
      print "error: '%s' is not file!" % (user_input)   

  def do_restartWkAndDe(self, user_input):
    """ restart workflow/dsched and rmLog/Storage"""
    self.do_stopDsched("")
    self.do_stopWorkflow("")
    self.do_rmWorkflowLog("")
    self.do_rmWorkflowStorage("")
    self.do_rmDschedLog("")
    self.do_rmDschedStorage("")
    self.do_startWorkflow("")
    self.do_startDsched("")

if __name__ == "__main__":
  argv = sys.argv
  argn = len(argv)
  
  netvmctl = NetVMTest(release_home, netvm_list, username, password)
  netvmctl.cmdloop()

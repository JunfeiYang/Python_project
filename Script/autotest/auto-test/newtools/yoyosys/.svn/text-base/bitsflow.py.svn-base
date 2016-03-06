#!/usr/bin/env python
import sys
sys.path.append("../")
import os
import time
import subprocess
import traceback
from util.login import *

class Bitsflow(Login):
  bitsflowHome = None
  cmd = ""

  def __init__(self, bitsflowHome, loginInfo, username=None, password=None, threadNum=6):
    Login.__init__(self, loginInfo, username, password, threadNum)

    if isinstance(bitsflowHome, str):
      if bitsflowHome[-1] == "/":
        bitsflowHome = bitsflowHome[:-1]
      self.bitsflowHome = bitsflowHome
    else:
      raise Exception, "bitsflowHome type must be string"

  def yoyosend(self, agent, service, user_input):
    sendcmd = ["yoyo_send", "-agent", agent, "-service", service];
    if isinstance(user_input,list):
      sendcmd.extend(user_input)
    else:
      sendcmd.extend(user_input.split())
    cmd = " ".join(sendcmd)
    print "yoyosend: [%s]"%cmd
    env = os.environ.copy()
    env["YOYO_DEFAULT_LOG_LVL"]="Error"
    result = subprocess.Popen(sendcmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env).communicate()[0]
    return result 

  def yoyosend_rpc(self, agent, service, user_input, rpc_timeout=10):
    if isinstance(user_input, list):
      tmplist=list()
      tmplist.append("-timeout")
      tmplist.append("%d"%rpc_timeout)
      tmplist.append("-rpc")
      tmplist.extend(user_input)
      return self.yoyosend(agent, service, tmplist)
    else:
      return self.yoyosend(agent, service, "-rpc -timeout %d %s"%(rpc_timeout, user_input))

  def getBitsflowLog(self, pc):
    print "\n====== IP: " + pc + " getBitsflowLog ======"
    #tarLogCmd = "cd %s;gdb --pid=`cat run/agent.pid` --command=./attach_bt | tee agent.stack;gdb --pid=`cat run/groupd.pid` --command=./attach_bt | tee groupd.stack;mkdir %s;rm -rf %s/*;cp -rf *.stack conf/*.xml logs/*log* bin/core* %s;tar cvzf %s %s" %(home, tarFolder, tarFolder, tarFolder, tarLog, tarFolder)
    tarFolder = "BitsflowLog-"+pc 
    tarLogCmd = "rm -rf BitsflowLog*;mkdir %s;cd %s;cp -rf conf/*.xml logs/*log* bin/core* ~/%s;cd ~;tar cvzf BitsflowLog.tar.gz %s" %(tarFolder, self.bitsflowHome, tarFolder, tarFolder)
    self.singleExecute(pc, tarLogCmd)

  def getBitsflowLogs(self, agent_list):
    try:
      self.startWork(self.getBitsflowLog, agent_list)
      self.getFile("BitsflowLog.tar.gz", None, agent_list)
    except:
      print sys.exc_info()
    finally:
      pass

  def controlBitsflow(self, controlCmd, input_pcList=None, mode="parallel", logLevel="Info"):
    cmd = "ulimit -c unlimited;cd %s;source bf_setenv.sh;export YOYO_DEFAULT_LOG_LVL=%s;cd bin/;%s" % \
          (self.bitsflowHome, logLevel, controlCmd)
    if mode == "parallel":
      self.parallelExecute(cmd, input_pcList)
    else:
      self.serialExecute(cmd, input_pcList)
    
  def restartNetvm(self, input_pcList=None, mode="parallel", logLevel="Info"):
    self.controlBitsflow("./netvmctl restart", input_pcList, mode, logLevel)

  def stopNetvm(self, input_pcList=None, mode="parallel"):
    self.controlBitsflow("./netvmctl stop", input_pcList, mode)
  def startNetvm(self, input_pcList=None, mode="parallel", logLevel="Info"):
    self.controlBitsflow("./netvmctl start", input_pcList, mode, logLevel)

  def restartGroupd(self, input_pcList=None, mode="parallel", logLevel="Info"):
    self.controlBitsflow("./bitsflowctl restart groupd", input_pcList, mode, logLevel)
  def stopGroupd(self, input_pcList=None, mode="parallel"):
    self.controlBitsflow("./bitsflowctl stop groupd", input_pcList, mode)
  def startGroupd(self, input_pcList=None, mode="parallel", logLevel="Info"):
    self.controlBitsflow("./bitsflowctl start groupd", input_pcList, mode, logLevel)

  def restartAgent(self, input_pcList=None, mode="parallel", logLevel="Info"):
    self.controlBitsflow("./bitsflowctl restart agent", input_pcList, mode, logLevel)
  def stopAgent(self, input_pcList=None, mode="parallel"):
    self.controlBitsflow("./bitsflowctl stop agent", input_pcList, mode)
  def startAgent(self, input_pcList=None, mode="parallel", logLevel="Info"):
    self.controlBitsflow("./bitsflowctl start agent", input_pcList, mode, logLevel)

  def rmBitsflowLogs(self, input_pcList=None):
    self.parallelExecute("rm -rf %s/logs/agent.log*"%self.bitsflowHome, input_pcList)

if __name__ == "__main__":
  pcList = ['127.0.0.1']
  
  bitsflow = Bitsflow("yoyopkg", pcList, "zhangtao", "calvinQQ^@@", len(pcList))
  #bitsflow.startAgent()

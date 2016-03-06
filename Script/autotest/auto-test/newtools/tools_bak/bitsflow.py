#!/usr/bin/env python
from login import *
from config import *
import sys


class Bitsflow(Login):
  bitsflowHome     = None
  bitsflowHomeDict = None
  cmd = ""

  def __init__(self, bitsflowHome, loginInfo, username=None, password=None, threadNum=6):
    Login.__init__(self, loginInfo, username, password, threadNum)

    if isinstance(bitsflowHome, dict):
      self.bitsflowHomeDict = bitsflowHome
    elif isinstance(bitsflowHome, str):
      if bitsflowHome[-1] == "/":
        bitsflowHome = bitsflowHome[:-1]
      self.bitsflowHome = bitsflowHome
    else:
      raise Exception, "bitsflowHome type must be dict or string"

  def getBitsflowLog(self, pc):
    print "\n====== IP: " + pc + " getBitsflowLog ======"
    tarFolder = "BitsflowLog-"+pc 
    tarLog = tarFolder+".tar.gz"

    if self.bitsflowHome is None:
      home = self.bitsflowHomeDict[pc]
      if home[-1] == "/":
        home = home[:-1]
    else:
      home = self.bitsflowHome

    #tarLogCmd = "cd %s;gdb --pid=`cat run/agent.pid` --command=./attach_bt | tee agent.stack;gdb --pid=`cat run/groupd.pid` --command=./attach_bt | tee groupd.stack;mkdir %s;rm -rf %s/*;cp -rf *.stack conf/*.xml logs/*log* bin/core* %s;tar cvzf %s %s" %(home, tarFolder, tarFolder, tarFolder, tarLog, tarFolder)
    tarLogCmd = "cd %s;mkdir %s;rm -rf %s/*;cp -rf conf/*.xml logs/*log* bin/core* %s;tar cvzf %s %s" %(home, tarFolder, tarFolder, tarFolder, tarLog, tarFolder)

    self.singleExecute(pc, tarLogCmd)

    remoteLogName = "%s/%s"%(home, tarLog)
    login_connections[pc].get(remoteLogName)

  def getBitsflowLogs(self):
    try:
      self.startWork(self.getBitsflowLog, agent_list)
    except:
      print sys.exc_info()
    finally:
      pass

  def controlBitsflow(self, controlCmd, input_pcList=None, mode="parallel", logLevel="Info"):
    if not self.bitsflowHome is None:
      cmd = "ulimit -c unlimited;cd %s;source bf_setenv.sh;export YOYO_DEFAULT_LOG_LVL=%s;cd bin/;%s" % \
            (self.bitsflowHome, logLevel, controlCmd)
      if mode == "parallel":
        self.parallelExecute(cmd, input_pcList)
      else:
        self.serialExecute(cmd, input_pcList)
    
    else:
      if input_pcList is None:
        pcs = agent_list
      else:
        pcs = input_pcList

      for pc in pcs:
        cmd = "ulimit -c unlimited;cd %s;source bf_setenv.sh;export YOYO_DEFAULT_LOG_LVL=%s;cd bin/;%s" % \
              (self.bitsflowHomeDict[pc], logLevel, controlCmd)
        self.singleExecute(pc, cmd)

  def restartNetvm(self, input_pcList=None, mode="parallel", logLevel=netvm_log_level):
    self.controlBitsflow("./netvmctl restart", input_pcList, mode, logLevel)

  def stopNetvm(self, input_pcList=None, mode="parallel", logLevel=netvm_log_level):
    self.controlBitsflow("./netvmctl stop", input_pcList, mode, logLevel)
  def startNetvm(self, input_pcList=None, mode="parallel", logLevel=netvm_log_level):
    self.controlBitsflow("./netvmctl start", input_pcList, mode, logLevel)

  def restartGroupd(self, input_pcList=None, mode="parallel", logLevel=groupd_log_level):
    self.controlBitsflow("./bitsflowctl restart groupd", input_pcList, mode, logLevel)
  def stopGroupd(self, input_pcList=None, mode="parallel", logLevel=groupd_log_level):
    self.controlBitsflow("./bitsflowctl stop groupd", input_pcList, mode, logLevel)
  def startGroupd(self, input_pcList=None, mode="parallel", logLevel=groupd_log_level):
    self.controlBitsflow("./bitsflowctl start groupd", input_pcList, mode, logLevel)

  def restartAgent(self, input_pcList=None, mode="parallel", logLevel=agent_log_level):
    self.controlBitsflow("./bitsflowctl restart agent", input_pcList, mode, logLevel)
  def stopAgent(self, input_pcList=None, mode="parallel", logLevel=agent_log_level):
    self.controlBitsflow("./bitsflowctl stop agent", input_pcList, mode, logLevel)
  def startAgent(self, input_pcList=None, mode="parallel", logLevel=agent_log_level):
    self.controlBitsflow("./bitsflowctl start agent", input_pcList, mode, logLevel)

  def rmBitsflowLogs(self, input_pcList=None, mode="parallel"):
    self.controlBitsflow("rm -rf ../logs/*log* ../BitsflowLog*", input_pcList, mode)

  def install(self, file32, file64, installPath, extractCmd, license, agentXML, groupdXML):
    if self.bitsflowHome is None:
      raise Exception, "BitsflowHome must be the same."
    uploadAndExtractFiles(file32, file64, installPath, extractCmd)
    self.parallelExecute("%s/install.pl"%self.bitsflowHome)
    self.putFiles(license,"%s/conf/yoyo.lic"%self.bitsflowHome);
    self.putFiles(agentXML,"%s/conf/agent.xml"%self.bitsflowHome);
    self.putFiles(groupdXML,"%s/conf/groupd.xml"%self.bitsflowHome);

if __name__ == "__main__":
  pcList = ['192.168.1.170']
  
  bitsflow = Bitsflow("bitsflow-2.5.0", pcList, "angel", "yangchunping", 3)
  #bitsflow.startAgent()

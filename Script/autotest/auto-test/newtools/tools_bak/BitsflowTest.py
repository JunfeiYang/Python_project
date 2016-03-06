#!/usr/bin/env python
import sys
from cmd import Cmd
import os
import traceback
from bitsflow import Bitsflow

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


bitsflow_log_home=""
IP_FILE = ".yoyo_ip_file"

class BitsflowTest(Cmd, Bitsflow):
  prompt = "[yoyo-sh]> "
  intro =  "Welcome to yoyo-shell, please use 'help' to show all commands!\n\n"
  intro += "Follow me to install bitsflow:\n"
  intro += "  1) prepare yoyopkg-xxx-noarch.tar.gz\n"
  intro += "  2) run 'installYoyopkg /home/zhangtao/yoyopkg-xxx-noarch.tar.gz'\n"
  intro += "  3) run 'yoyopkg install --tag BITSFLOW_2_3_1'\n"
  intro += "  4) prepare agent.xml.sample and yoyo.lic in current path\n"
  intro += "  5) run 'configBitsflow agent.xml.sample yoyo.lic'\n"
  intro += "  6) run 'startAgent'\n"
  intro += "  7) run 'ps'\n"

  def __init__(self):
    Cmd.__init__(self)
    bitsflow_log_home = os.path.join(release_home, "logs")
    Bitsflow.__init__(self, release_home, pc_list, username, password, len(pc_list))

  def do_backupBitsflowLog(self, user_input):
    """Usage: backupBitsflowLog dir"""
    if len(user_input) == 0:
      print "Usage: backupBitsflowLog dir"
    else:
      cmd = "mkdir %s; cp %s %s; %s > %s"%(user_input, os.path.join(bitsflow_log_home, "*log*"), user_input, self.createYoyopkgCmd("ls"), os.path.join(user_input, "version"))
      self.parallelExecute(cmd, agent_list)

  def createGDBScript(self):
    f = open("yoyo_gdb_attach", "w")
    f.write("thread apply all bt\nquit")
    f.close()

  def do_EOF(self, user_input):
    print "Bye!"
    return True

  def do_quit(self, user_input):
    """Quit yoyo-shell"""
    return self.do_EOF(user_input)
  def do_q(self, user_input):
    """Quit yoyo-shell"""
    return self.do_quit(user_input)

  def emptyline(self):
    pass

  def do_shell(self, line):
    "Run a shell command"
    output = os.popen(line).read()
    print output

  def do_singleCmd(self, user_input):
    """Usage: singleCmd ip cmdStr"""
    inputs = user_input.split()
    if len(inputs) < 2:
      print "Usage: singleCmd ip cmdStr"
    else:
      outputs = self.singleExecute(inputs[0], " ".join(inputs[1:]))
      for output in outputs:
        print output.strip()

  def do_parallelCmd(self, user_input):
    """Usage: parallelCmd cmdStr"""
    inputs = user_input.split()
    if len(inputs) < 1:
      print "Usage: parallelCmd cmdStr"
    else:
      self.parallelExecute(" ".join(inputs[0:]))

  def do_serialCmd(self, user_input):
    """Usage: serialCmd cmdStr"""
    inputs = user_input.split()
    if len(inputs) < 1:
      print "Usage: serialCmd cmdStr"
    else:
      self.serialExecute(" ".join(inputs[0:]))

  def do_ps(self, user_input):
    """Usage: ps [processName] (If no processName, we'll "ps agent")"""
    if len(user_input) == 0:
      cmd = "ps aux|grep agent"
    else:
      cmd = "ps aux|grep %s"%user_input
    self.serialExecute(cmd)

  def do_restartAgent(self, user_input):
    self.restartAgent()
  def do_startAgent(self, user_input):
    self.startAgent()
  def do_stopAgent(self, user_input):
    """stop Agent [ip1 ip2 ... ipN]"""
    if len(user_input) == 0:
      self.stopAgent()
    else:
      inputs = user_input.split()
      self.stopAgent(inputs)

  def do_killAgent(self, user_input):
    """kill -9 Agent [ip1 ip2 ... ipN]"""
    if len(user_input) == 0:
      self.parallelExecute("kill -9 `cat %s/run/agent.pid`"%release_home)
    else:
      inputs = user_input.split()
      self.parallelExecute("kill -9 `cat %s/run/agent.pid`"%release_home, inputs)

  def do_restartAgent2(self, user_input):
    self.do_stopAgent2()
    self.do_startAgent2()
  def do_startAgent2(self, user_input):
    cmd = "ulimit -c unlimited;source %s;export YOYO_DEFAULT_LOG_LVL=%s;%s"\
          %(os.path.join(release_home, "bf_setenv.sh"), \
            agent_log_level,\
            "%s/bin/agent -cfgfile %s/conf/agent2.xml -logfile %s/logs/agent2.log -pidfile %s/run/agent2.pid -daemon -licfile %s/creds/yoyo2.lic -tokfile %s/creds/agent2.tok"%(release_home,release_home,release_home,release_home,release_home,release_home))
    self.parallelExecute(cmd)
  def do_stopAgent2(self, user_input):
    self.parallelExecute("kill `cat %s/run/agent2.pid`"%release_home)

  def do_restartAgent3(self, user_input):
    self.do_stopAgent3()
    self.do_startAgent3()
  def do_startAgent3(self, user_input):
    cmd = "ulimit -c unlimited;source %s;export YOYO_DEFAULT_LOG_LVL=%s;%s"\
          %(os.path.join(release_home, "bf_setenv.sh"), \
            agent_log_level,\
            "%s/bin/agent -cfgfile %s/conf/agent3.xml -logfile %s/logs/agent3.log -pidfile %s/run/agent3.pid -daemon -licfile %s/creds/yoyo3.lic -tokfile %s/creds/agent3.tok"%(release_home,release_home,release_home,release_home,release_home,release_home))
    self.parallelExecute(cmd)
  def do_stopAgent3(self, user_input):
    self.parallelExecute("kill `cat %s/run/agent3.pid`"%release_home)

  def do_startGroupd(self, user_input):
    self.startGroupd(groupd_list)
  def do_restartGroupd(self, user_input):
    self.restartGroupd(groupd_list)
  def do_stopGroupd(self, user_input):
    """stop Groupd [ip1 ip2 ... ipN]"""
    if len(user_input) == 0:
      self.stopGroupd()
    else:
      inputs = user_input.split()
      self.stopGroupd(inputs)
  def do_killGroupd(self, user_input):
    """kill -9 Groupd [ip1 ip2 ... ipN]"""
    if len(user_input) == 0:
      self.parallelExecute("kill -9 `cat %s/run/groupd.pid`"%release_home)
    else:
      inputs = user_input.split()
      self.parallelExecute("kill -9 `cat %s/run/groupd.pid`"%release_home, inputs)

  def do_startNetvm(self, user_input):
    self.startNetvm(netvm_list)
  def do_restartNetvm(self, user_input):
    self.restartNetvm(netvm_list)
  def do_stopNetvm(self, user_input):
    self.stopNetvm(netvm_list)

  def do_getBitsflowLog(self, user_input):
    """Download bitsflow logs"""
    self.getBitsflowLogs()
  def do_rmBitsflowLog(self, user_input):
    """Remove bitsflow logs"""
    self.rmBitsflowLogs()

  def configBitsflow(self, localAgentConf, remoteAgentConf, localLicense, remoteLicense, agentPort):
    try:
      self.createGDBScript()
      self.putFile("yoyo_gdb_attach")

      self.parallelExecute("%s/bf_install.pl"%release_home)
      confPath  = os.path.join(release_home, "conf")
      credsPath = os.path.join(release_home, "creds")
      self.parallelExecute("mkdir -p %s;mkdir -p %s"%(confPath, credsPath))
      fullRemoteAgentConf = os.path.join(confPath, remoteAgentConf)
      fullRemoteLicFile   = os.path.join(credsPath, remoteLicense)
      for ip in agent_list:
        tmpAgentConf = "%s.%s"%(localAgentConf, ip)
        os.system("cp %s %s"%(localAgentConf, tmpAgentConf))
        replace = "sed -i 's/<Network-Interface>.*<\/Network-Interface>/<Network-Interface>%s<\/Network-Interface>/g' %s"%(ip, tmpAgentConf)
        os.system(replace)
        replace = "sed -i 's/<Listen>.*<\/Listen>/<Listen>%s<\/Listen>/g' %s"%(agentPort, tmpAgentConf)
        os.system(replace)
        replace = "sed -i 's/<Ping-Listen>.*<\/Ping-Listen>/<Ping-Listen>%s<\/Ping-Listen>/g' %s"%(agentPort, tmpAgentConf)
        os.system(replace)
        self.putFileToPC(tmpAgentConf, fullRemoteAgentConf, ip)
      self.putFile(localLicense, fullRemoteLicFile)
    except:
      traceback.print_exc()

  def do_configBitsflow(self, user_input):
    """Usage: configBitsflow agent.xml.sample yoyo.lic"""
    inputs = user_input.split()
    inputs_len = len(inputs)

    if inputs_len != 2:
      print "Usage: configBitsflow agent.xml.sample yoyo.lic"
      return
    else:
      self.configBitsflow(inputs[0], "agent.xml", inputs[1], "yoyo.lic", agent_port)

  def do_configBitsflow2(self, user_input):
    """Usage: configBitsflow2 agent2.xml.sample yoyo.lic"""
    inputs = user_input.split()
    inputs_len = len(inputs)

    if inputs_len != 2:
      print "Usage: configBitsflow2 agent2.xml.sample yoyo.lic"
      return
    else:
      self.configBitsflow(inputs[0], "agent2.xml", inputs[1], "yoyo2.lic", agent2_port)

  def do_configBitsflow3(self, user_input):
    """Usage: configBitsflow3 agent3.xml.sample yoyo.lic"""
    inputs = user_input.split()
    inputs_len = len(inputs)

    if inputs_len != 2:
      print "Usage: configBitsflow3 agent3.xml.sample yoyo.lic"
      return
    else:
      self.configBitsflow(inputs[0], "agent3.xml", inputs[1], "yoyo3.lic", agent3_port)

  def do_configGroupd(self, user_input):
    """Usage: configGroupd groupd.xml.sample"""
    inputs = user_input.split()
    inputs_len = len(inputs)

    if inputs_len != 1:
      print "Usage: configGroupd groupd.xml.sample"
      return
    else:
      try:
        self.parallelExecute("%s/bf_install.pl"%release_home)
        confPath  = os.path.join(release_home, "conf")
        self.parallelExecute("mkdir -p %s"%(confPath))
        remoteGroupdConf = os.path.join(confPath, "groupd.xml")
        groupdNum = len(groupd_list)
        if groupdNum % 2 == 0:
          raise Exception, "Groupd number must be odd."

        if groupdNum > 1:
          usePaxos = "true"
        else:
          usePaxos = "false"

        for index, ip in enumerate(groupd_list):
          localGroupdConf = "groupd.xml.%s"%ip
          os.system("cp %s %s"%(inputs[0], localGroupdConf))
          replace = "sed -i 's/<Use-Paxos>.*<\/Use-Paxos>/<Use-Paxos>%s<\/Use-Paxos>/g' %s"%(usePaxos, localGroupdConf)
          os.system(replace)
          replace = "sed -i 's/<Replica-Id>.*<\/Replica-Id>/<Replica-Id>%d<\/Replica-Id>/g' %s"%(index, localGroupdConf)
          os.system(replace)
          replace = "sed -i 's/<Num-Replicas>.*<\/Num-Replicas>/<Num-Replicas>%d<\/Num-Replicas>/g' %s"%(groupdNum, localGroupdConf)
          os.system(replace)
          replace = "sed -i 's/<Agent>.*<\/Agent>/<Agent>localhost:%s<\/Agent>/g' %s"%(agent_port, localGroupdConf)
          os.system(replace)
          self.putFileToPC(localGroupdConf, remoteGroupdConf, ip)
      except:
        traceback.print_exc()

  def do_configNetVM(self, user_input):
    """Usage: configNetVM netvmd.xml.sample"""
    inputs = user_input.split()
    inputs_len = len(inputs)

    if inputs_len != 1:
      print "Usage: configNetVM netvmd.xml.sample"
      return
    else:
      try:
        self.parallelExecute("%s/bf_install.pl"%release_home)
        confPath  = os.path.join(release_home, "conf")
        self.parallelExecute("mkdir -p %s"%(confPath))
        remoteNetVMConf = os.path.join(confPath, "netvmd.xml")
        for ip in netvm_list:
          localNetVMConf = "netvmd.xml.%s"%ip
          os.system("cp %s %s"%(inputs[0], localNetVMConf))
          replace = "sed -i 's/<!-- <Host-Id>.*<\/Host-Id> -->/<Host-Id>%s<\/Host-Id>/g' %s"%(ip, localNetVMConf)
          os.system(replace)
          replace = "sed -i 's/<Host-Id>.*<\/Host-Id>/<Host-Id>%s<\/Host-Id>/g' %s"%(ip, localNetVMConf)
          os.system(replace)
          self.putFileToPC(localNetVMConf, remoteNetVMConf, ip)
      except:
        traceback.print_exc()

  def do_installYoyopkg(self, user_input):
    """Usage: installYoyopkg yoyopkg-xxx-noarch.tar.gz"""
    inputs = user_input.split()
    inputs_len = len(inputs)

    if inputs_len != 1:
      print "Usage: installYoyopkg yoyopkg-xxx-noarch.tar.gz"
      return
    else:
      try:
        self.parallelExecute("mkdir -p %s;"%release_home)
        remoteFile = os.path.join(release_home, os.path.basename(inputs[0]))
        self.putFile(inputs[0], remoteFile)
        self.parallelExecute("cd %s;tar xzvf %s"%(release_home, os.path.basename(inputs[0])))
      except:
        traceback.print_exc()

  def createYoyopkgCmd(self, user_input):
    inputs = user_input.split()
    inputs_len = len(inputs)
    env = "--release %s --platform %s --repository %s --user %s --password %s"%(release_home, platform, repository, repo_username, repo_password)
    if inputs_len < 1:
      print "Usage: yoyopkg cmdStr"
      return
    else:
      setEnvCmd = "source %s;"%(os.path.join(release_home,"bf_setenv.sh"))

      if inputs_len == 1:
        cmd = "%s%s %s %s"%(setEnvCmd, os.path.join(release_home, "bin/yoyopkg"), inputs[0], env)
      elif inputs_len > 1:
        cmd = "%s%s %s %s %s"%(setEnvCmd, os.path.join(release_home, "bin/yoyopkg"), inputs[0], env, " ".join(inputs[1:]))
    return cmd


  def doyoyopkg(self, user_input, pclist=None):
    cmd = self.createYoyopkgCmd(user_input)
    print cmd
    self.serialExecute(cmd, pclist)

  def do_yoyopkg(self, user_input):
    """Usage: yoyopkg cmdStr"""
    inputs = user_input.split()
    inputs_len = len(inputs)
    if inputs_len < 1:
      print "Usage: yoyopkg cmdStr"
      return
    else:
      self.doyoyopkg(user_input)

  def do_getFile(self, user_input):
    """Usage: getFile remoteFile [localFile] """
    inputs = user_input.split()
    if len(inputs) < 1:
      print "Usage: getFile remoteFile [localFile]"
    else:
      if len(inputs) == 2:
        remoteFile = inputs[0]
        localFile  = inputs[1]
      else:
        remoteFile = inputs[0]
        localFile = os.path.basename(inputs[0])
      self.getFile(remoteFile, localFile)

  def do_putFile(self, user_input):
    """Usage: putFile localFile [remoteFile]"""
    inputs = user_input.split()
    if len(inputs) < 1:
      print "Usage: putFile localFile [remoteFile]"
    else:
      remoteFile = localFile = inputs[0]
      if len(inputs) == 2:
        remoteFile = inputs[1]
      self.putFile(localFile, remoteFile)

  def do_deployScript(self, user_input):
    """Upload ./script/* to all remote pc"""
    for ip in pc_list:
      cmd = "echo %s > %s"%(ip, IP_FILE)
      self.singleExecute(ip, cmd)

    for root, dirs, files in os.walk("./script"):
      if root == "./script":
        for f in files:
          print "Upload %s ..."%f
          self.putFile(os.path.join("./script", f), f)
          self.parallelExecute("chmod +x %s"%f)

  def do_cutAgentPort(self, user_input):
    """Usage: cutAgentPort sleepTime(s) [loop] [ip1 ip2 ... ipN]"""
    inputs = user_input.split()
    inputsLen = len(inputs)
    if inputsLen < 1:
      print "Usage: cutAgentPort sleepTime(s) [loop] [ip1 ip2 ... ipN]"
    elif inputsLen == 1:
      cmd = "sudo ./iptable.sh %s %s"%(agent_port, inputs[0])
      self.parallelExecute(cmd, agent_list)
    elif inputsLen == 2:
      cmd = "sudo ./iptable.sh %s %s %s"%(agent_port, inputs[0], inputs[1])
      self.parallelExecute(cmd, agent_list)
    else:
      cmd = "sudo ./iptable.sh %s %s %s"%(agent_port, inputs[0], inputs[1])
      self.parallelExecute(cmd, inputs[2:])
      
  def do_restartInterface(self, user_input):
    """Usage: restartInterface sleepTime(s) [loop] [ip1 ip2 ... ipN]"""
    inputs = user_input.split()
    inputsLen = len(inputs)
    if inputsLen < 1:
      print "Usage: restartInterface sleepTime(s) [loop] [ip1 ip2 ... ipN]"
    elif inputsLen == 1:
      cmd = "sudo ./networkRestart.sh %s %s"%(inputs[0], IP_FILE)
      self.parallelExecute(cmd)
    elif inputsLen == 2:
      cmd = "sudo ./networkRestart.sh %s %s %s"%(inputs[0], IP_FILE, inputs[1])
      self.parallelExecute(cmd)
    else:
      cmd = "sudo ./networkRestart.sh %s %s %s"%(inputs[0], IP_FILE, inputs[1])
      self.parallelExecute(cmd, inputs[2:])
  
  def do_trafficControl(self, user_input):
    """Usage: trafficControl sleepTime(s) action(delay|loss|duplicate|corrupt|reorder) [loop] [ip1 ip2 ... ipN]"""
    inputs = user_input.split()
    inputsLen = len(inputs)
    if inputsLen < 2:
      print "Usage: trafficControl sleepTime(s) action(delay|loss|duplicate|corrupt|reorder) [loop] [ip1 ip2 ... ipN]"
    elif inputsLen == 2:
      cmd = "sudo ./tc.sh %s %s %s"%(IP_FILE, inputs[1], inputs[0])
      self.parallelExecute(cmd)
    elif inputsLen == 3:
      cmd = "sudo ./tc.sh %s %s %s %s"%(IP_FILE, inputs[1], inputs[0], inputs[2])
      self.parallelExecute(cmd)
    else:
      cmd = "sudo ./tc.sh %s %s %s %s"%(IP_FILE, inputs[1], inputs[0], inputs[2])
      self.parallelExecute(cmd, inputs[3:])


if __name__ == "__main__":
  bfctl = BitsflowTest()
  bfctl.cmdloop()

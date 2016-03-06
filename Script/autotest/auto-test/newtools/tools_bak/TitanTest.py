#!/usr/bin/env python
from login import *
from titan_conf import *
import sys
from cmd import Cmd
import os
import traceback


class TitanTest(Login, Cmd):
  prompt = "[yoyo-sh]> "

  def __init__(self):
    Cmd.__init__(self)
    Login.__init__(self, pc_list, username, password, len(pc_list))

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

  def do_installTitan(self, user_input):
    """Usage: installTitan titan-cassandra-0.2.1.zip"""
    inputs = user_input.split()
    inputs_len = len(inputs)

    if inputs_len != 1:
      print "Usage: installTitan titan-cassandra-0.2.1.zip"
      return
    else:
      try:
        self.parallelExecute("mkdir -p %s;"%release_home)
        remoteFile = os.path.join(release_home, os.path.basename(inputs[0]))
        self.putFile(inputs[0], remoteFile)
        self.parallelExecute("cd %s;unzip %s"%(release_home, os.path.basename(inputs[0])))
        
        cmd = 'cd %s;echo "./bin/titan.sh config/titan-server-rexster.xml config/titan-server-cassandra.properties" > start.sh'%(titan_home)
        self.parallelExecute(cmd);

        self.putFile("titan.sh", "%s/bin/titan.sh"%titan_home)
      except:
        traceback.print_exc()

  def do_startTitan(self, user_input):
    """start titan"""
    self.parallelExecute("cd %s;nohup ./start.sh"%(titan_home))

  def do_stopTitan(self, user_input):
    self.parallelExecute("kill `cat %s/titan.pid`"%titan_home)


  def do_clearCassandra(self, user_input):
    rmdirs = "rm -rf %s/* %s/* %s/* %s/*"%(cassandra_data_dir, cassandra_commitlog_dir, cassandra_saved_caches_dir, cassandra_log_dir)
    self.parallelExecute(rmdirs)

  def do_configCassandra(self, user_input):
    """Usage: configCassandra cassandra.yaml"""
    inputs = user_input.split()
    inputs_len = len(inputs)

    if inputs_len != 1:
      print "Usage: configCassandra cassandra.yaml"
      return
    else:
      try:
        mkdirs = "mkdir -p %s %s %s %s"%(cassandra_data_dir, cassandra_commitlog_dir, cassandra_saved_caches_dir, cassandra_log_dir)
        self.parallelExecute(mkdirs)

        if titan_embed:
          remoteConf = os.path.join(titan_home, "config", "cassandra.yaml")
        else:
          remoteConf = os.path.join(cassandra_home, "conf", "cassandra.yaml")
        
        loop = 0
        node_num = len(pc_list)
        for ip in pc_list:
          localConf = "%s.%s"%("cassandra.yaml", ip)
          os.system("cp %s %s"%(inputs[0], localConf))

          replace = "sed -i 's#- /tmp/cassandra/data.*#- %s#g' %s"%(cassandra_data_dir, localConf)
          os.system(replace)

          replace = "sed -i 's#- /var/lib/cassandra/data.*#- %s#g' %s"%(cassandra_data_dir, localConf)
          os.system(replace)

          replace = "sed -i 's#commitlog_directory:.*#commitlog_directory: %s#g' %s"%(cassandra_commitlog_dir, localConf)
          os.system(replace)

          replace = "sed -i 's#saved_caches_directory:.*#saved_caches_directory: %s#g' %s"%(cassandra_saved_caches_dir, localConf)
          os.system(replace)
          
          replace = "sed -i 's#- seeds:.*#- seeds: \"%s\"#g' %s"%(cassandra_seeds, localConf)
          os.system(replace)

          replace = "sed -i 's#listen_address:.*#listen_address: %s#g' %s"%(ip, localConf)
          os.system(replace)

          replace = "sed -i 's#rpc_address:.*#rpc_address: %s#g' %s"%(ip, localConf)
          os.system(replace)

          replace = "sed -i 's#partitioner:.*#partitioner: org.apache.cassandra.dht.Murmur3Partitioner#g' %s"%(localConf)
          os.system(replace)

          replace = "sed -i 's#initial_token:.*#initial_token: %d#g' %s"%((int(2**64 / node_num * loop) - 2**63), localConf)
          os.system(replace)

          self.putFileToPC(localConf, remoteConf, ip)
          loop+=1
      except:
        traceback.print_exc()



if __name__ == "__main__":
  titan = TitanTest()
  titan.cmdloop()

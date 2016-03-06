#!/usr/bin/env python
import os
import time
import subprocess
import sys
import traceback
from cmd import Cmd
from config import *

class BitsflowUtil(Cmd):
  prompt = "[yoyo-sh]> "

  def __init__(self):
    Cmd.__init__(self)

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

  def yoyosend_rpc(self, agent, service, user_input):
    if isinstance(user_input, list):
      tmplist=list()
      tmplist.append("-timeout")
      tmplist.append("%d"%rpc_timeout)
      tmplist.append("-rpc")
      tmplist.extend(user_input)
      return self.yoyosend(agent, service, tmplist)
    else:
      return self.yoyosend(agent, service, "-rpc -timeout %d %s"%(rpc_timeout, user_input))

  def do_yoyosend(self, user_input):
    inputs = user_input.split()
    inputs_len = len(inputs)

    if inputs_len < 3:
      print "Usage: yoyosend agent service ..."
      return

    print self.yoyosend(user_input[0], user_input[1], user_input[2:])

if __name__ == "__main__":
  util = BitsflowUtil()
  util.cmdloop()

#!/usr/bin/env python
from config import *
from utilconfig import *
from NetVMTest import *
import sys
import os
import traceback
import re
import uuid

class MBTest(NetVMTest):
  intro =  "Welcome to yoyo-shell, please use 'help' to show all commands!\n\n"

  def __init__(self, bitsflowHome, pcList, username, password):
    NetVMTest.__init__(self, bitsflowHome, pcList, username, password)

  def setFailed(self, name, failedString):
    os.system("echo -n 'control:%s' > %s"%(failedString, name))
    os.system("yoyo_send -agent %s -service %s -timeout %s -rpc %s -int32 0 -str %s -str \"\" -int32 0 -file-opaque ./%s"\
        %(agent, service, timeout, name, uuid.uuid1(), name))

  def do_mbSetAllocateFailed(self, user_input):
    """usage: mbSetAllocateFailed failedString"""
    if len(user_input) < 1:
      print "usage: mbSetAllocateFailed failedString"
    else:
      self.setFailed("allocateService", user_input)

  def do_mbSetReallocateFailed(self, user_input):
    """usage: mbSetReallocateFailed failedString"""
    if len(user_input) < 1:
      print "usage: mbSetReallocateFailed failedString"
    else:
      self.setFailed("reallocateService", user_input)

  def do_mbSetUpdateDBFailed(self, user_input):
    """usage: mbSetUpdateDBFailed failedString"""
    if len(user_input) < 1:
      print "usage: mbSetUpdateDBFailed failedString"
    else:
      self.setFailed("updateDatabaseService", user_input)

  def do_mbSetReloadFailed(self, user_input):
    """usage: mbSetReloadFailed failedString"""
    if len(user_input) < 1:
      print "usage: mbSetReloadFailed failedString"
    else:
      self.setFailed("failedReallocateService", user_input)

  def do_mbHappyPath(self, user_input):
    """usage: mbHappyPath workflowId"""
    array = user_input.split()
    if len(array) < 1:
      print "usage: mbHappyPath workflowId"
    else:
      self.do_wkEvalExpression("%s job_num=3 3"%array[0])
      self.do_wkEvalExpression("%s basic_retry_times=3 3"%array[0])
      self.do_wkPlaceTokens("%s CurrentTask 2 CurrentTask 2 CurrentTask 2"%array[0])
      self.do_wkPlaceTokens("%s Jobs (1,2,'10.1',3) Jobs (2,2,'20.2',3) Jobs (3,2,'30.3',3)"%array[0])

  def do_mbZeroScore(self, user_input):
    """usage: mbZeroScore workflowId"""
    array = user_input.split()
    if len(array) < 1:
      print "usage: mbZeroScore workflowId"
    else:
      self.do_wkEvalExpression("%s job_num=3 3"%array[0])
      self.do_wkEvalExpression("%s basic_retry_times=3 3"%array[0])
      self.do_wkPlaceTokens("%s CurrentTask 2 CurrentTask 2 CurrentTask 2"%array[0])
      self.do_wkPlaceTokens("%s Jobs (1,2,'0',3) Jobs (2,2,'0',3) Jobs (3,2,'0',3)"%array[0])

  def do_mbDoJob(self, user_input):
    """usage: mbDoJob workflowId taskId [jobNum]"""
    array = user_input.split()
    if len(array) < 2:
      print "usage: mbDoJob workflowId taskId [jobNum]"
    else:
      workflow_id = array[0]
      task_id = array[1]
      try:
        if len(task_id) <= 0:
          print "taskID is invalid!"
          return
      except:
        print "taskID is invalid!"
        return

      job_num = 50 
      if len(array) >= 2:
        try:
          job_num = int(array[2])
          if job_num <= 0:
            print "jobNum is invalid, use default jobNum: %d" % job_num
            job_num = 50
        except:
          print "jobNum is invalid, use default jobNum: %d" % job_num
        
      self.do_wkEvalExpression("%s job_num=%d 3" % (workflow_id, job_num))
      self.do_wkEvalExpression("%s basic_retry_times=3 3" % workflow_id)
      self.do_wkPlaceTokens("%s %s" % (workflow_id, " ".join(["CurrentTask %s" % (task_id)] * job_num)))
      job_str = ""
      for i in range(job_num):
        job_str = job_str + "Jobs (%d,%s,'%d.%d',3) " % (i+1, task_id, i+1, i+1)
      self.do_wkPlaceTokens("%s %s" % (workflow_id, job_str))


if __name__ == "__main__":
  argv = sys.argv
  argn = len(argv)
  
  pcList = agentList + groupdList

  mbctl = MBTest(release_home, pcList, username, password)
  mbctl.cmdloop()

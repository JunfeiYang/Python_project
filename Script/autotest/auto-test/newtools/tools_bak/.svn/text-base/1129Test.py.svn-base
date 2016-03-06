#!/usr/bin/env python
from config import *
from NetVMTest import *
from DataCellTest import *
import sys
import os
import traceback
import re
import uuid

CPN_ID="cpndemo"
WORKFLOW_ID="wkdemo"

class DemoTest(NetVMTest,DataCellTest):
  intro =  "Welcome to yoyo-shell, please use 'help' to show all commands!\n\n"

  def __init__(self, bitsflowHome, pcList, username, password):
    NetVMTest.__init__(self, bitsflowHome, pcList, username, password)

  def do_1129AddNextTarget(self, user_input):
    """usage: 1129AddNextTarget nodeId nextTarget..."""
    array = user_input.split()
    arrayLen = len(array)
    if arrayLen < 2:
      print "usage: 1129AddNextTarget nodeId nextTarget..."
    else:
      for i in range(1,arrayLen):
        self.do_wkPlaceTokens("%s Start ('add','%s','%s')"%(WORKFLOW_ID, array[0], array[i]))

  def do_1129DelNextTarget(self, user_input):
    """usage: 1129DelNextTarget nodeId nextTarget..."""
    array = user_input.split()
    arrayLen = len(array)
    if arrayLen < 2:
      print "usage: 1129DelNextTarget nodeId nextTarget..."
    else:
      for i in range(1,arrayLen):
        self.do_wkPlaceTokens("%s Start ('del','%s','%s')"%(WORKFLOW_ID, array[0], array[i]))

  def do_1129GetMembers(self, user_input):
    """usage: 1129GetMembers"""
    self.do_wkEvalExpression("%s members" % (WORKFLOW_ID,))

  def do_1129init(self, user_input):
    """usage: 1129init"""
    self.do_wkStopWF(WORKFLOW_ID)
    self.do_wkDeleteWF(WORKFLOW_ID)
    self.do_wkDeleteCPN(CPN_ID)
    self.do_wkCreateCPN("./1129demo.xml")
    self.do_wkCreateWF("%s %s"%(CPN_ID, WORKFLOW_ID))
    self.do_wkStartWF(WORKFLOW_ID)

if __name__ == "__main__":
  argv = sys.argv
  argn = len(argv)
  
  ctl = DemoTest(release_home, pc_list, username, password)
  ctl.cmdloop()

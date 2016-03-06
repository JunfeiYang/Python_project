#!/usr/bin/env python

from cmd import Cmd
import sys
import os
import subprocess
import time
import atexit
import simplejson
import urllib2

import NetVMTest
from utilconfig import *

test_server_subject = "YoyoAutoTest.server"

class AutoTest(NetVMTest.NetVMTest):
  prompt = "[yoyo-sh]> "
  intro  = "Welcome to Yoyosys autotest!\n\n"

  def yoyosend_autotest_rpc(self, user_input):
    if isinstance(user_input, list):
      tmplist=list()
      tmplist.append("-timeout")
      tmplist.append("%d"%timeout)
      tmplist.append("-rpc")
      tmplist.append(test_server_subject)
      tmplist.extend(user_input)
      return self.yoyosend(tmplist)
    else:
      return self.yoyosend("-rpc -timeout %d %s  -str %s %s"%(timeout, test_server_subject, os.environ.get("USER"), user_input))

  def do_shell(self, user_input):
    "Run a shell command"
    output = os.popen(user_input).read()
    print output

  def do_auListRunningTestSuite(self, user_input):
    """List Running Test Suite"""
    result =  self.yoyosend_autotest_rpc(" -str %s" % ("listRunningTestSuite"))
    print result
    lines = result.splitlines()
    result_status = lines[-2][len("Reply Field 1: INT32 "):]
    result_content = lines[-1][len("Reply Field 2: STR "):]
    #print "status: ", result_status
    #print "hosts: ", result_content
    if result_status == "0":
      suite_list = simplejson.loads(result_content)
      if len(suite_list) > 0:
        print "============================ result ==========================="
        print "Running Suite:"
        print "%36s\t%s\t%s" % ("Suite Id", "Suite Name", "User Name")
        for suite_info in suite_list:
          print "%s\t%s\t%s" % (suite_info["suiteId"], suite_info["suiteName"], suite_info["user"])

  def do_auListFinishedTestSuite(self, user_input):
    """List Finished Test Suite, Usage: auListFinishedTestSuite page_num"""
    page_num = 1
    if len(user_input) > 0:
      try:
        page_num = int(user_input)
        if page_num <= 0:
          print "Usage: auListFinishedTestSuite page_num"
          return
      except:
        print "Usage: auListFinishedTestSuite page_num"
        return
    result =  self.yoyosend_autotest_rpc(" -str %s -int32 %d" % ("listFinishedTestSuite", page_num))
    print result
    lines = result.splitlines()
    result_status = lines[-2][len("Reply Field 1: INT32 "):]
    result_content = lines[-1][len("Reply Field 2: STR "):]
    #print "status: ", result_status
    #print "hosts: ", result_content
    if result_status == "0":
      result_info = simplejson.loads(result_content)
      suite_list = result_info["finishedSuites"]
      pageSize = result_info["pageSize"]
      pageNum = result_info["pageNum"]
      totalSuites = result_info["totalNum"]
      print "============================ result ==========================="
      print "Total Suites Number: %d, Current Page: %d, Page Size: %d" % (totalSuites, pageNum, pageSize)
      if len(suite_list) > 0:
        print "Finished Suite:"
        print "%36s\t%s\t%s\t%s\t%s" % ("Suite Id", "Suite Name", "User Name", "Start Time", "End Time")
        for suite_info in suite_list:
          print "%s\t%s\t%s\t%s\t%s" % (suite_info["suiteId"], suite_info["suiteName"], suite_info["user"], suite_info["startTime"], suite_info["endTime"])
  
  
  def do_auListHosts(self, user_input):
    result =  self.yoyosend_autotest_rpc(" -str %s" % ("listHost"))
    print result
    lines = result.splitlines()
    result_status = lines[-2][len("Reply Field 1: INT32 "):]
    result_content = lines[-1][len("Reply Field 2: STR "):]
    #print "status: ", result_status
    #print "hosts: ", result_content
    print "============================ result ==========================="
    if result_status == "0":
      print "hosts:"
      host_list = simplejson.loads(result_content)
      for host_info in host_list:
        print host_info
 
  def do_auRunTestSuite(self, user_input):
    #startMonitorThread = threading.Thread(target=self.singleExecute, args=(pc, tarLogCmd))
    #startMonitorThread.setDaemon(True)
    #startMonitorThread.start()
    result =  self.yoyosend_autotest_rpc(" -str %s -file-str %s" % ("runTest", user_input))
    print result
    lines = result.splitlines()
    result_status = lines[-2][len("Reply Field 1: INT32 "):]
    result_content = lines[-1][len("Reply Field 2: STR "):]
    print "status: ", result_status
    print "workflowId: ", result_content
 
  def do_auQueryTestSuite(self, user_input):
    print "todo"

  def do_auQueryTestSuiteResult(self, user_input):
    """ "Query Test Suite Result, usage: auQueryTestSuiteResult suiteId"""
    if len(user_input) <= 0:
      print "Usage: auQueryTestSuiteResult suiteId [outputFile_1 outputFile_2 .. outputFile_n]"
      return

    param_list = user_input.split(" ")
    
    result = self.yoyosend_autotest_rpc(" -str %s -str %s" % ("getTestResult", param_list[0]))
    print result
    lines = result.splitlines()
    result_status = lines[-2][len("Reply Field 1: INT32 "):]
    result_content = lines[-1][len("Reply Field 2: STR "):]
    #print "status: ", result_status
    #print "result: ", result_content
    print "============================ result ==========================="
    if result_status == "0":
      suite_result = simplejson.loads(result_content)
      test_result_list = suite_result["caseResultList"]
      suiteName = suite_result["suiteName"]
      suiteId = suite_result["suiteId"]
      startTime = suite_result["startTime"]
      endTime = suite_result["endTime"]
      print "Suite Name:", suiteName
      print "Start Time:", startTime
      if endTime == "":
        print "End Time:  ", "running"
      else:
        print "End Time:  ", endTime

      if not (type(test_result_list) == type([])):
        print test_result_list
        test_result_list = simplejson.loads(test_result_list)
      if len(test_result_list) <= 0:
        return

      print "getting result:"
      result_dir = os.path.join(".", "testsuite_result", "%s_%s" % (suiteName, suiteId))
      print "result dir: %s" % (result_dir)
      if not os.path.isdir(result_dir):
        os.makedirs(result_dir)

      for i in range(len(test_result_list)):
        print "test %d" % (i)
        result_test_dir = os.path.join(result_dir, "test_%d" % (i+1))
        if not os.path.isdir(result_test_dir):
          os.makedirs(result_test_dir)
        for j in range(len(test_result_list[i])):
          print "  case %d, casename, %s" % (j, test_result_list[i][j][0][2])
          result_case_dir = os.path.join(result_test_dir, "case_%d_%s" % (j+1, test_result_list[i][j][0][2]))
          if not os.path.isdir(result_case_dir):
            os.makedirs(result_case_dir)
          for k in range(len(test_result_list[i][j])):
            host_name = test_result_list[i][j][k][0]
            print "    host %s: " % host_name, test_result_list[i][j][k]
            result_node_dir = os.path.join(result_case_dir, "host_%d_%s" % (k+1, host_name))
            if not os.path.isdir(result_node_dir):
              os.makedirs(result_node_dir)

            for file_name in ["__STDIN__", "__STDOUT__"] + param_list[1:]:
              try:
                file_name = file_name.strip()
                result_url = "http://%s:%s/%s/%s/%s" % (host_name, netvm_http_port, remote_dir, test_result_list[i][j][k][7], file_name)
                #print "result url:", result_url
                req = urllib2.Request(result_url, None, {})
                result_file = os.path.join(result_node_dir, file_name)
                f = open(result_file, "w")
                f.write(urllib2.urlopen(req).read())
                f.close()
              except:
                print "get %s failed!" % result_url


  def do_auCancelTestSuite(self, user_input):
    print "todo"

  def do_auCancelTest(self, user_input):
    print "todo"

  def do_auCancelCase(self, user_input):
    print "todo"

  def do_auGetLog(self, user_input):
    print "todo"


if __name__ == "__main__":
  argv = sys.argv
  argn = len(argv)
  #atexit.register(cleanup)
      
  pcList = NetVMTest.agentList + NetVMTest.groupdList

  #netvmctl = NetVMTest(release_home, pcList, username, password)
  #netvmctl.cmdloop()

  test = AutoTest(NetVMTest.release_home, pcList, NetVMTest.username, NetVMTest.password)
  test.cmdloop()

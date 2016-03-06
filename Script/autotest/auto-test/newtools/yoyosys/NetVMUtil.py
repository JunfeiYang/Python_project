#!/usr/bin/python
from BitsflowTest import *
from config import *
from xml.dom.minidom import parseString

workflow_subject_prefix="WORKFLOW." + workflow_groupname + ".COMMAND."
dsched_subject_prefix="DSCHED." + dsched_groupname + ".COMMAND."

create_cpn  = workflow_subject_prefix + "CREATE_CPN"
delete_cpn  = workflow_subject_prefix + "DELETE_CPN"
get_cpn_xml = workflow_subject_prefix + "GET_CPN_XML"
create_wf = workflow_subject_prefix + "CREATE_WF"
place_tokens = workflow_subject_prefix + "PLACE_TOKENS"
start_wf = workflow_subject_prefix + "START_WF"
stop_wf = workflow_subject_prefix + "STOP_WF"
delete_wf = workflow_subject_prefix + "DELETE_WF"
get_cpns = workflow_subject_prefix + "GET_CPNS"
get_tokens = workflow_subject_prefix + "GET_TOKENS"
query_wf_status = workflow_subject_prefix + "QUERY_WF_STATUS"
eval_expression = workflow_subject_prefix + "EVAL_EXPRESSION"
get_marking = workflow_subject_prefix + "GET_MARKING"
get_executions = workflow_subject_prefix + "GET_EXECUTIONS"
get_execution_info = workflow_subject_prefix + "GET_EXECUTION_INFO"
get_errors = workflow_subject_prefix + "GET_ERRORS"
clear_errors = workflow_subject_prefix + "CLEAR_ERRORS"
clear_exited_executions = workflow_subject_prefix + "CLEAR_EXITED_EXECUTIONS"
step = workflow_subject_prefix + "STEP"
delete_tokens = workflow_subject_prefix + "DELETE_TOKENS"

create_job_spec = dsched_subject_prefix + "CREATE_JOB_SPEC"
delete_job_spec = dsched_subject_prefix + "DELETE_JOB_SPEC"
get_job_specs = dsched_subject_prefix + "GET_JOB_SPECS"
get_job_spec = dsched_subject_prefix + "GET_JOB_SPEC"
run_job = dsched_subject_prefix + "RUN_JOB"
get_jobs = dsched_subject_prefix + "GET_JOBS"
query_job_status = dsched_subject_prefix + "QUERY_JOB_STATUS"
query_dsched_status = dsched_subject_prefix + "QUERY_DSCHED_STATUS"
get_job_output = dsched_subject_prefix + "GET_JOB_OUTPUT"
terminate_all_jobs = dsched_subject_prefix + "TERMINATE_ALL_JOBS"
terminate_job = dsched_subject_prefix + "TERMINATE_JOB"
delete_job = dsched_subject_prefix + "DELETE_JOB"
clear_exited_job = dsched_subject_prefix + "CLEAR_EXITED_JOBS"
     
class NetVMUtil(BitsflowTest):
  def __init__(self):
    BitsflowTest.__init__(self)
    self.netvm_agent="%s:%s"%(netvm_list[0], agent_port)
  def do_wkCreateCPN(self, user_input):
    """usage: wkCreateCPN cpnfile"""
    if len(user_input) < 1:
      print "usage: wkCreateCPN cpnfile"
    else:
      print self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -file-str %s"%(create_cpn, user_input))

  def do_wkDeleteCPN(self, user_input):
    """usage: wkDeleteCPN cpnId"""
    if len(user_input) < 1:
      print "usage: wkDeleteCPN cpnId"
    else:
      print self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s"%(delete_cpn, user_input))
  
  def do_wkDeleteTokens(self, user_input):
    """usage: wkDeleteToken workflowid placeId """
    array = user_input.split()
    if len(array) < 2:
      print "usage: wkDeleteToken workflowId placeId"
    else:
      print self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s -str %s -str ''"%(delete_tokens, array[0], array[1]))

  def do_wkGetCPNXml(self, user_input):
    """usage: wkGetCPNXml cpnId"""
    if len(user_input) < 1:
      print "usage: wkGetCPNXml cpnId"
    else:
      result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s"%(get_cpn_xml, user_input))
      print result
  
  def do_wkCreateWF(self, user_input):
    """usage: wkCreateWK cpnId [workflowId]"""
    if len(user_input) < 1:
      print "usage: wkCreateWK cpnId [workflowId]"
    else:
      array = user_input.split()
      if len(array) == 1:
        result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s -int32 0"%(create_wf, user_input))
      elif len(array) == 2:
       	result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s  -str %s  -int32 0 -str %s"%(create_wf, array[0], array[1]))
      print result
 
  def do_wkStartWF(self, user_input):
    """usage: wkStartWF workfolwId [isKeepRuning(int32 default:1)] [step mode(int32 default:0)] [periodical scan transition(int32 default:0)]"""
    if len(user_input) < 1:
      print "usage: wkStartWF workfolwId [isKeepRuning(int32 default:1)] [step mode(int32 default:0)] [periodical scan transition(int32 default:0)]"
    else:
      arrlist=list()
      arrlist.append(start_wf)
      arrs = user_input.split()
      arrlist.append(arrs[0])
      if len(arrs) == 1:
        arrlist.append("-int32")
        arrlist.append("1")
      else:
        if len(arrs) > 1:
          arrlist.append("-int32")
          arrlist.append(arrs[1])
      if len(arrs) > 2:
        arrlist.append("-int32")
        arrlist.append(arrs[2])
      if len(arrs) > 3:
        arrlist.append("-int32")
        arrlist.append(arrs[3])
      result = self.yoyosend_rpc(self.netvm_agent, netvm_service, arrlist)
      print result
  
  def do_wkStopWF(self, user_input):
    """usage: wkStopWF workfolwId"""
    if len(user_input) < 1:
      print "usage: wkStopWF workflowId"
    else:
      result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s"%(stop_wf, user_input))
      print result
  
  def do_wkQueryWFStatus(self, user_input):
    """usage: wkQueryWFStatus workfolwId"""
    if len(user_input) < 1:
      print "usage: wkQueryWFStatus workflowId"
    else:
      result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s"%(query_wf_status, user_input))
      print result
  
  def do_wkGetMarking(self, user_input):
    """usage: wkGetMarking workfolwId"""
    if len(user_input) < 1:
      print "usage: wkGetMarking workflowId"
    else:
      marking=""
      isOK=False
      if os.path.isfile("marking"):
        os.remove("marking")
      result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s -int32 1"%(get_marking, user_input))
      lines=result.split("\n")
      for line in lines:
        if line.startswith("Reply Field 2:"):
          marking=line[19:]
          f = open("marking", "w")
          f.write(marking)
          f.close()
          isOK=True
      if isOK:
        os.system("xmllint -format marking")
        pass
      else:
        print result
      #print result
  
  def do_wkGetErrors(self, user_input): 
    """usage: wkGetErrors workfolwId"""
    if len(user_input) < 1:
      print "usage: wkGetErrors workflowId"
    else:
      result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s"%(get_errors, user_input))
      print result
  
  def do_wkStep(self, user_input): 
    """usage: wkStep workfolwId"""
    if len(user_input) < 1:
      print "usage: wkStep workflowId"
    else:
      result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s"%(step, user_input))
      print result
  

  def do_wkEvalExpression(self, user_input): 
    """usage: wkEvalExpression workfolwId expression"""
    array = user_input.split()
    if len(array) < 2:
      print "usage: wkEvalExpression workflowId expression expression_flag"
    else:
      if len(array) == 2:
        result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s -str %s -int32 1"%(eval_expression, array[0], array[1]))
      else:
        result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s -str %s -int32 %s"%(eval_expression, array[0], array[1], array[2]))
      print result
  
  def do_wkGetExecutionInfo(self, user_input): 
    """usage: wkGetExecutionInfo workfolwId executionId"""
    array = user_input.split()
    if len(array)< 2:
      print "usage: wkGetExecutionInfo workflowId executionId"
    else:
      result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s -str %s"%(get_execution_info, array[0], array[1]))
      print result
  
  def do_wkGetExecutions(self, user_input): 
    """usage: wkGetExecutions workfolwId"""
    if len(user_input)< 1:
      print "usage: wkGetExecutions workflowId "
    else:
      result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s"%(get_executions, user_input))
      print result
  
  def do_wkClearErrors(self, user_input): 
    """usage: wkClearErrors workfolwId"""
    if len(user_input)< 1:
      print "usage: wkGetErrors workflowId"
    else:
      result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s"%(clear_errors, user_input))
      print result
  
  def do_wkClearExitedExecutions(self, user_input): 
    """usage: wkClearExitedExecutions workfolwId"""
    if len(user_input)< 1:
      print "usage: wkClearExitedExecutions workflowId"
    else:
      result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s"%(clear_exited_executions, user_input))
      print result

  def do_wkDeleteWF(self, user_input):
    """usage: wkDeleteWF workfolwId"""
    if len(user_input) < 1:
      print "usage: wkDeleteWF workflowId"
    else:
      result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s"%(delete_wf, user_input))
      print result
  
  def do_wkPlaceTokens(self, user_input):
    """usage: wkPlaceToken workfolwId placeId tokenValue [placeId] [tokenValue]"""
    array = user_input.split()
    if len(array) < 3:
      print "usage: wkPlaceToken workflowId placeId tokenValue [placeId] [tokenValue]"
    else:
      arrayList = list()
      i = len(array)
      if i%2 == 1:
       for j in range(1,i):
         arrayList.append("-str ")
         arrayList.append(array[j])
       arrayFinal = " ".join(arrayList)
       result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s -int32 0 %s"%(place_tokens, array[0], arrayFinal))
       print result
      else:
        print "placeId and tokenId need to match"
  
  def do_wkGetTokens(self, user_input):
    """usage: wkGetTokens workflowId placeId"""
    array = user_input.split()
    if len(array) < 2:
      print "usage: wkGetTokens workflowId placeId"
    else:
      array = user_input.split()
      result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s -str %s -int32 1 -int32 0"%(get_tokens, array[0], array[1]))
      print result
  
  def do_dsQueryDschedStatus(self, user_input):
    """usage: dsQueryDschedStatus """
    result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s"%(query_dsched_status))
    print result
  
  def do_wkGetCPNs(self, user_input):
    """usage: wkGetCPNs"""
    result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s"%(get_cpns))
    print result
  
  def do_wkDeleteAllCPNs(self, user_input):
    """usage: wkDeleteAllCPN """
    result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s"%(get_cpns))
    cpns_str = result.splitlines()[-1]
    if cpns_str.startswith("Reply Field 2: STR "):
      cpns_xml = cpns_str[len("Reply Field 2: STR "):]
      cpns_dom = parseString(cpns_xml)
      cpns_node = cpns_dom.childNodes[0]
      for cpn_node in cpns_node.childNodes:
        cpn_id = cpn_node.getAttribute("id") 
        print "cpnId %s" % cpn_id
        for workflow_node in cpn_node.childNodes:
          workflow_id = workflow_node.getAttribute("id")
          print "  workflowId: %s" % workflow_id
          self.do_wkStopWF(workflow_id)
          self.do_wkDeleteWF(workflow_id)
        self.do_wkDeleteCPN(cpn_id)
      result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s"%(get_cpns))
      print result
    else:
      print result

  def do_wkDeleteAllWorkflows(self, user_input):
    """usage: wkDeleteAllCPN """
    result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s"%(get_cpns))
    cpns_str = result.splitlines()[-1]
    if cpns_str.startswith("Reply Field 2: STR "):
      cpns_xml = cpns_str[len("Reply Field 2: STR "):]
      cpns_dom = parseString(cpns_xml)
      cpns_node = cpns_dom.childNodes[0]
      for cpn_node in cpns_node.childNodes:
        cpn_id = cpn_node.getAttribute("id") 
        print "cpnId %s" % cpn_id
        for workflow_node in cpn_node.childNodes:
          workflow_id = workflow_node.getAttribute("id")
          print "  workflowId: %s" % workflow_id
          self.do_wkStopWF(workflow_id)
          self.do_wkDeleteWF(workflow_id)
      result = self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s"%(get_cpns))
      print result
    else:
      print result

  def do_dsGetJobOutput(self, user_input):
    """usage: dsGetJobOutput jobId outputName [type]"""
    array = user_input.split()
    if len(array) < 2:
      print "usage: dsGetJobOutput jobId outputName [type]"
    elif len(array) == 3:
      print self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s -str %s -int32 %d"%(get_job_output, array[0], array[1], int(array[2])))
    else:
      print self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s -str %s -int32 %d"%(get_job_output, array[0], array[1], 1))

  def do_dsCreateJobSpec(self, user_input):
    """usage: dsCreateJobSpec jobSpecXml"""
    if len(user_input) < 1:
      print "usage: dsCreateJobSpec jobSpecXml"
    else:
      print self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -file-str %s"%(create_job_spec, user_input))

  def do_dsDeleteJobSpec(self, user_input):
    """usage: dsDeleteJobSpec jobSpecId"""
    if len(user_input) < 1:
      print "usage: dsDeleteJobSpec jobSpecId"
    else:
      print self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s"%(delete_job_spec, user_input))
  
  def do_dsGetJobs(self, user_input):
    """usage: dsGetJobs [jobSpecName]"""
    if len(user_input) < 1:
      print self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s" %(get_jobs))
    else:
      print self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s"%(get_jobs, user_input))
  
  def do_dsGetJobSpecs(self, user_input):
    """usage: dsGetJobSpecs """
    print self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s"%(get_job_specs))
  
  def do_dsGetJobSpec(self, user_input):
    """usage: dsGetJobSpec jobSpecId"""
    if len(user_input) < 1:
      print "usage: dsGetJobSpec jobSpecId"
    else:
      print self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s"%(get_job_spec, user_input))
  
  def do_dsQueryJobStatus(self, user_input):
    """usage: dsQueryJobStatus jobId"""
    if len(user_input) < 1:
      print "usage: dsQueryJobStatus jobId"
    else:
      print self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s"%(query_job_status, user_input))
  
  def do_dsDeleteJob(self, user_input):
    """usage: dsDeleteJob jobId"""
    if len(user_input) < 1:
      print "usage: dsDeleteJob jobId"
    else:
      print self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s"%(delete_job, user_input))
  
  def do_dsTerminateJob(self, user_input):
    """usage: dsTerminateJob jobId"""
    if len(user_input) < 1:
      print "usage: dsTerminateJob jobId"
    else:
      print self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s"%(terminate_job, user_input))

  def do_dsTerminateAllJobs(self, user_input):
    """usage: dsTerminateAllJobs [jobSpecName]"""
    if len(user_input) < 1:
      print self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s"%(terminate_all_jobs))
    else:
      print self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s -str %s"%(terminate_all_jobs, user_input))

  def do_dsClearExitedJobs(self, user_input):
    """usage: dsClearExitedJobs"""
    print self.yoyosend_rpc(self.netvm_agent, netvm_service, "%s"%(clear_exited_job))

  def do_dsRunJob(self, user_input):
    """usage: dsRunJob jobSpecId [priority=0] [--hostId [jobInputName::inputContent]...]..."""
    inputs = user_input.split()
    inputs_len = len(inputs)
    usage = "usage: dsRunJob jobSpecId [priority=0] [--restrictHost host1...hostN] [--inputs inputName1::inputContent1 ... inputNameN::inputContentN]"
    arguments = list()
    arguments.append(run_job)

    if inputs_len < 1:
      print usage

    else:
      arguments.append("-str")
      arguments.append(inputs[0])
      arguments.append("-str")
      arguments.append("")

      if inputs_len > 1:
        arguments.append("-int32")
        arguments.append(inputs[1])

        if inputs_len > 2:
          host_num = 0
          input_num = 0
          infos = inputs[2:]
          host_arg   = list()
          input_arg  = list()
          hostBegin  = False
          inputBegin = False
          for i in infos:
            if i == "--restrictHost":
              hostBegin  = True
              inputBegin = False
              continue
            elif i == "--inputs":
              hostBegin  = False
              inputBegin = True
              continue

            if hostBegin:
              host_num += 1
              host_arg.append("-str")
              host_arg.append(i)
            elif inputBegin:
              input_num += 1
              tmp_input = i.split("::")
              if len(tmp_input) !=2:
                print usage
                return
              input_arg.append("-str")
              input_arg.append(tmp_input[0])
              input_arg.append("-file-opaque")
              input_arg.append(tmp_input[1])
          arguments.append("-int32")
          arguments.append(str(host_num))
          if len(host_arg) > 0:
            arguments.extend(host_arg)

          arguments.append("-int32")
          arguments.append(str(input_num))

          if len(input_arg) > 0:
            arguments.extend(input_arg)

        else:
          arguments.append("-int32")
          arguments.append("0")
          arguments.append("-int32")
          arguments.append("0")
      else:
        arguments.append("-int32")
        arguments.append("0")
        arguments.append("-int32")
        arguments.append("0")
        arguments.append("-int32")
        arguments.append("0")
      #print arguments
      print self.yoyosend_rpc(self.netvm_agent, netvm_service, arguments)

if __name__ == "__main__":
  util = NetVMUtil()
  util.cmdloop()

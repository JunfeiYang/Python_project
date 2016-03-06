import time
import json
import sys

import cmd_config
reload(cmd_config)

if cmd_config.autotest_home not in sys.path:
  sys.path.append(cmd_config.autotest_home)

import StdoutUtil
import NetVMTest

instance = None
try:
  instance = self
except:
  pcList = NetVMTest.agentList + NetVMTest.groupdList
  instance = NetVMTest.NetVMTest(NetVMTest.release_home, pcList, NetVMTest.username, NetVMTest.password)

# change stdout
sys.stdout = StdoutUtil.StdoutLogger("w")

#################### start #######################

# Create job spec
instance.do_dsCreateJobSpec(cmd_config.install_host_file)
instance.do_dsCreateJobSpec(cmd_config.do_case_file)

# Create cpn
instance.do_wkCreateCPN(cmd_config.cpn_file)

# Create workflow
instance.do_wkCreateWF("%s %s" % (cmd_config.cpn_name, cmd_config.workflow_name))

# Start workflow
instance.do_wkStartWF(cmd_config.workflow_name)

# EvalExpression
instance.do_wkEvalExpression("%s hostIds=%s 3" % (cmd_config.workflow_name, json.dumps(cmd_config.host_list).replace(" ","")))
instance.do_wkEvalExpression("%s hostIds 2" % (cmd_config.workflow_name))
#instance.do_wkEvalExpression("%s requiredHostNum=%d 3" % (cmd_config.workflow_name, cmd_config.required_host_num))
#instance.do_wkEvalExpression("%s requiredHostNum 2" % (cmd_config.workflow_name))
instance.do_wkEvalExpression("%s installRetryNum=%d 3" % (cmd_config.workflow_name, cmd_config.install_retry_num))
instance.do_wkEvalExpression("%s installRetryNum 2" % (cmd_config.workflow_name))
instance.do_wkEvalExpression("%s currentTest=%d 3" % (cmd_config.workflow_name, cmd_config.current_test))
instance.do_wkEvalExpression("%s currentTest 2" % (cmd_config.workflow_name))
instance.do_wkEvalExpression("%s currentCase=%d 3" % (cmd_config.workflow_name, cmd_config.current_case))
instance.do_wkEvalExpression("%s currentCase 2" % (cmd_config.workflow_name))
instance.do_wkEvalExpression("%s softwareList=%s 3" % (cmd_config.workflow_name, json.dumps(cmd_config.software_list).replace(" ","")))
instance.do_wkEvalExpression("%s softwareList 2" % (cmd_config.workflow_name))
instance.do_wkEvalExpression("%s caseNameList=%s 3" % (cmd_config.workflow_name, json.dumps(cmd_config.case_name_list).replace(" ","")))
instance.do_wkEvalExpression("%s caseNameList 2" % (cmd_config.workflow_name))

#instance.do_wkEvalExpression("%s casePolicyList=%s 3" % (cmd_config.workflow_name, json.dumps(cmd_config.case_policy_list).replace(" ","")))
#instance.do_wkEvalExpression("%s casePolicyList 2" % (cmd_config.workflow_name))
instance.do_wkEvalExpression("%s testPolicyList=%s 3" % (cmd_config.workflow_name, json.dumps(cmd_config.test_policy_list).replace(" ","")))
instance.do_wkEvalExpression("%s testPolicyList 2" % (cmd_config.workflow_name))
instance.do_wkEvalExpression("%s suitePolicy='%s' 3" % (cmd_config.workflow_name, cmd_config.suite_policy))
instance.do_wkEvalExpression("%s suitePolicy 2" % (cmd_config.workflow_name))
instance.do_wkEvalExpression("%s caseScriptList=%s 3" % (cmd_config.workflow_name, json.dumps(cmd_config.case_script_list).replace(" ","")))
instance.do_wkEvalExpression("%s caseScriptList 2" % (cmd_config.workflow_name))


# Start TestSuite

instance.do_wkPlaceTokens("%s Start 1" % (cmd_config.workflow_name))

# Wait
time.sleep(1)

# Get markings
instance.do_wkGetMarking(cmd_config.workflow_name)

# Get Result
instance.do_wkEvalExpression("%s caseResultList 2" % (cmd_config.workflow_name))

# restore stdout
sys.stdout = sys.stdout.old_stdout

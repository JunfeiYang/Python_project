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


# Get markings
instance.do_wkGetMarking(cmd_config.workflow_name)

# Get Result
instance.do_wkEvalExpression("%s caseResultList 2" % (cmd_config.workflow_name))

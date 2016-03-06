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

#################### stop #######################

# Terminage all jobs
instance.do_dsTerminateAllJobs("")

# Clear exited jobs
instance.do_dsClearExitedJobs("")

# Delete job spec
instance.do_dsDeleteJobSpec(cmd_config.install_host_job)
instance.do_dsDeleteJobSpec(cmd_config.do_case_job)

# Stop workflow
instance.do_wkStopWF(cmd_config.workflow_name)

# Delete workflow
instance.do_wkDeleteWF(cmd_config.workflow_name)

# Delete cpn
instance.do_wkDeleteCPN(cmd_config.cpn_name)



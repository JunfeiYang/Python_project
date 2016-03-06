#!/usr/bin/env python

import env_set,shell
import os

env_dist = {
	'OS_AUTH_URL':'http://172.16.209.11:5000/v2.0',
	'OS_TENANT_ID':'f1134680ff48420382bad868071bb115',
	'OS_TENANT_NAME':'kycloudprod',
	'OS_USERNAME':'kycloudprod',
	'OS_PASSWORD':'che001'
	}
value_list = ['OS_AUTH_URL','OS_TENANT_ID','OS_TENANT_NAME','OS_USERNAME','OS_PASSWORD']

keys = env_dist.keys()
for i in keys:
	value = env_dist[i]
	env_set.set_env(i,value)
#os.system("nova list")
cmd = 'nova  volume-list'
content = shell.shell_cmd(cmd)

f = open('/tmp/list','a')
f.writelines(content)
f.close()
 


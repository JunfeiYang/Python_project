#!/usr/bin/python
#
#========================================================================
# Author:Andre
# Email:yangjunfei2146@gmail.com
# File Name: 
# Description:
# Edit History:
# 2015-02-21 File created.
#========================================================================

import sys
import shell_cmd as shell

# ip address get 
def ip_address():
    cmd =  "ifconfig eth0|sed -n '/inet / p'|cut -d : -f2|awk '{print $1}'" 
    ip = shell.shell_cmd(cmd)
    ip_address = ip[0].split('\n')
    return ip_address[0]

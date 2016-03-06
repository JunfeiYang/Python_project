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

# hostname 
def hostname_get():
    cmd = "hostname"
    hostname_get = shell.shell_cmd(cmd)[0].split('\n')[0]
    return hostname_get

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

# System  login user name.
def login_user_name():
	cmd = "who -uq|sed -n '/[a-z,A-Z]/ p'"
 	login_user_name = shell.shell_cmd(cmd)[0].split('\n')[0]
	return login_user_name
def login_user_num():
	cmd = "who -uq|sed -n '/#/ p'|cut -d = -f2"
	login_user_num = shell.shell_cmd(cmd)[0].split('\n')[0]
	return login_user_num


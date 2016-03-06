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

# Average CPU load.
def cpu_loadavg():
	cmd = "uptime |awk -F 'load average:' '{print $2}'"
	cpu_loadavg = shell.shell_cmd(cmd)
	return cpu_loadavg[0].split('\n')[0]
# User CPU usage.
def cpu_user():
	cmd = "iostat -c 1 3 |grep -v -e '^[a-z]' -e '^[A-Z]' -e '^$'|awk 'BEGIN{sum=0}{sum +=$1/3}END{print sum}'"
	cpu_user = shell.shell_cmd(cmd)
	return cpu_user[0].split('\n')[0]
# Nice CPU usage.
def cpu_nice():
	cmd = "iostat -c 1 3 |grep -v -e '^[a-z]' -e '^[A-Z]' -e '^$'|awk 'BEGIN{sum=0}{sum +=$2/3}END{print sum}'"
	cpu_nice = shell.shell_cmd(cmd)
	return cpu_nice[0].split('\n')[0]
# System CPU usage.
def cpu_system():
	cmd = "iostat -c 1 3 |grep -v -e '^[a-z]' -e '^[A-Z]' -e '^$'|awk 'BEGIN{sum=0}{sum +=$3/3}END{print sum}'"
	cpu_system = shell.shell_cmd(cmd)
	return cpu_system[0].split('\n')[0]
# Iowait CPU usage.
def cpu_iowait():
	cmd = "iostat -c 1 3 grep -v -e '^[a-z]' -e '^[A-Z]' -e '^$'|awk 'BEGIN{sum=0}{sum +=$4/3}END{print sum}'"
	cpu_iowait = shell.shell_cmd(cmd)
	return cpu_iowait[0].split('\n')[0]
# Steal CPU usage.
def cpu_steal():
	cmd = "iostat -c 1 3 |grep -v -e '^[a-z]' -e '^[A-Z]' -e '^$'|awk 'BEGIN{sum=0}{sum +=$5/3}END{print sum}'"
	cpu_steal = shell.shell_cmd(cmd)
	return cpu_steal[0].split('\n')[0]
# Idle CPU usage.
def cpu_idle():
	cmd = "iostat -c 1 3 |grep -v -e '^[a-z]' -e '^[A-Z]' -e '^$'|awk 'BEGIN{sum=0}{sum +=$6/3}END{print sum}'"
	cpu_idle = shell.shell_cmd(cmd)
	return cpu_idle[0].split('\n')[0]
# 



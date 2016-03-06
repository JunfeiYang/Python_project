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

#  Mem Total Usage .
def mem_total():
	cmd = "free -m |grep Mem |awk '{print $2}'"
	mem_total = shell.shell_cmd(cmd)
	return mem_total[0].split('\n')[0] 
# Mem Freed Size.
def  mem_freed():
	cmd = "free -m |grep Mem |awk '{print $4}'"
	mem_freed = shell.shell_cmd(cmd)
	return mem_freed[0].split('\n')[0]
# Mem Used  size.
def mem_used():
	cmd = "free -m |grep Mem |awk '{print $3}'"
	mem_used = shell.shell_cmd(cmd)
	return mem_used[0].split('\n')[0]
# Mem buffers freed size.
def mem_buffers_freed():
	cmd = "free -m |grep 'buffers/cache:'|awk '{print $4}'"
	mem_buffers_freed = shell.shell_cmd(cmd)
	return mem_buffers_freed[0].split('\n')[0]
# Mem buffers used size.
def mem_buffers_used():
	cmd = "free -m |grep 'buffers/cache:'|awk '{print $3}'"
	mem_buffers_used = shell.shell_cmd(cmd)
	return mem_buffers_used[0].split('\n')[0]
# Mem useded percent.
def mem_used_percent():
	cmd = "free -m |grep Mem |awk '{printf  $3/$2*100}'"
	mem_used_percent = shell.shell_cmd(cmd)
	return mem_used_percent[0].split('\n')[0]
# SWAP Total size.
def swap_total():
	cmd = "free -m |grep 'Swap'|awk '{print $2}'" 
	swap_total = shell.shell_cmd(cmd)
	return swap_total[0].split('\n')[0]
# Swap freed size.
def swap_freed():
	cmd = "free -m |grep 'Swap'|awk '{print $4}'"
	swap_freed = shell.shell_cmd(cmd)
	return swap_freed[0].split('\n')[0]
# Swap used size.
def swap_used():
	cmd = "free -m |grep 'Swap'|awk '{print $3}'"
	swap_used = shell.shell_cmd(cmd)
	return swap_used[0].split('\n')[0]
# Swap used percent .
def swap_used_percent():
	cmd = "free -m |grep 'Swap'|awk '{print $3/$2*100}'"
	swap_used_percent = shell.shell_cmd(cmd)
	return swap_used_percent[0].split('\n')[0]

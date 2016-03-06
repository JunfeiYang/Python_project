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
import psutil

# Disk Total size.
def disk_total():
	disk_total = psutil.disk_usage('/')
	return disk_total[0]
# Disk partitions .
def disk_partitions():
	part =  psutil.disk_partitions()
	num = len(part)
	for p in range(num):
		print part[p][0]
# Disk used size.
def disk_used():
	disk_used = psutil.disk_usage('/')
	return disk_used[1]

# Disk freed size.
def disk_freed():
	disk_freed = psutil.disk_usage('/')
	return disk_freed[2]

# Disk used Percent.
def disk_used_percent():
	disk_used_percent = psutil.disk_usage('/')
	return disk_used_percent[3]
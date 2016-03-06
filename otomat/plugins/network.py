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


# NIC toatl recv traffic .
def  nic_traffic_recv():
	nic_recv = psutil.network_io_counters()
	return nic_recv[1]
# The total capacity of nic receive error .
def  nic_traffic_recv_err():
	nic_recv_err = psutil.network_io_counters()
	return nic_recv_err[4]
# Nic total sent traffic
def nic_traffic_sent():
	nic_sent = psutil.network_io_counters()
	return nic_sent[0]
# The total capacity of nic receive error .
def  nic_traffic_sent_err():
	nic_sent_err = psutil.network_io_counters()
	return nic_sent_err[5]
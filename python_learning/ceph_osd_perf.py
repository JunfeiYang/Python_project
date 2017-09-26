# !/usr/bin/env python
# --*-- coding:utf-8 -*-
#  Author: Andre Yang
#  Email: yangjunfei2146@gmail.com
#  File Name: ceph_osd_perf
#  Description:
#  Edit History: 2017-09-20
# ==================================================
import  commands
import  sys,json


data = []
cmd = commands.getstatusoutput('ceph osd perf')
ceph_data = cmd[1].split(''.join('\n'))
for i in range(len(ceph_data)):
    c = ceph_data[i].split()
    data.append(c)
    
# data = [ "id,fs_commit_latency,fs_apply_latency","1 51 5", "2 60 6","3 66 7"]

def osd_list():
    print "{\n"+"\"data\":["
    for j in range(1,(len(data)-1)):
        v = data[j][0]
        print "{\"{#OSDID}\":\"%s\"}, " %v
    v_last = data[len(data)-1][0]
    print "{\"{#OSDID}\":\"%s\"} ] " %v_last
    print "} \n"

def osd_perf_fun(num, osd_perf_option):
    data_list = []
    for i in range(1,len(data)):
        if num == data[i][0] and osd_perf_option == "fs_commit_latency":
            print  data[i][1]
        elif num == data[i][0] and osd_perf_option == "fs_apply_latency":
            print data[i][2]

def usage():
    usages='''
precondition:
    The ceph client environment must be configured to enable ceph osd perf;
Usage:
    python ceph_osd_perf.py [option <perf|list>] [osdid <osdid name>] [suboption <fs_commit_latency(ms)|fs_apply_latency(ms)>]
Example:
    # list osd
    python ceph_osd_perf.py  list 
    # list  osd 1 perf  fs_commit_latency
    python ceph_osd_perf.py  perf 1 fs_commit_latency
    # list  osd 1 perf  fs_apply_latency
    python ceph_osd_perf.py  perf 1 fs_apply_latency
    '''
    print usages
if __name__ == '__main__':
    if len(sys.argv) == 2 :
        osdid_list = sys.argv[1]
        if  osdid_list == "list":
            print osd_list()
            #print data_get()
        else:
            usage()
    elif len(sys.argv) == 4 :
        osd_perf_option = sys.argv[3]
        osd_perf = sys.argv[1]
        osd_perf_num = int(sys.argv[2])
        num_list = [x for x in range(1,1000)]
        if osd_perf_num in num_list:
            num = osd_perf_num
        else:
            print "The second parameter type is incorrect, enter int"
        if  osd_perf == "perf":
            num = str(num)
            osd_perf_fun(num,osd_perf_option)
        else:
            usage() 
    else:
        usage()

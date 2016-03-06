# !/usr/bin/env python
# --*-- coding:utf-8 -*-
#  Author: Andre Yang
#  Email: yangjunfei2146@gmail.com
#  File Name:
#  Description:
#  Edit History:
# ==================================================
import os,sys,time
from shell_cmd import shell_cmd as shell
from functools import wraps

class tranffic_action(object):
    '''
    def __init__(self):
        pass
    '''
    def tranffic_init(self):
        port = 'eth0'
        cmd = 'tc qdisc ls dev %s |grep  "cbq 1:"' % port
        result = shell(cmd)
        if result:
            pass
        else:
            cmd_qdisc_del = 'tc qdisc del dev %s root handle 1: ' % port
            cmd_qdisc = 'tc qdisc add dev %s root \
                        handle 1: htb default 100' % port
            cmd_class_0 = 'tc class add dev eth0 parent 1:0 classid 1:1 htb \
                         rate 1000Mbit ceil 1000Mbit '
            cmd_class_1 = 'tc class add dev eth0 parent 1:0 classid 1:2 htb \
                        rate 1000Mbit rate 500Mbit '
            cmd_class_2 = 'tc class add dev eth0 parent 1:0 classid 1:3 htb \
                        rate 50Mbit ceil  50Mbit'
            cmd_class_3 = 'tc class add dev eth0 parent 1:0 classid 1:4 htb \
                        rate 5Mbit ceil 5Mbit'
            cmd_class_4 = 'tc class add dev eth0 parent 1:0 classid 1:5 htb \
                        rate 1Mbit ceil 1Mbit'
            cmd_class_5 = 'tc class add dev eth0 parent 1:0 classid 1:6 htb \
                        rate 100Kbit ceil 100Kbit'
            cmd_list = [cmd_qdisc_del,cmd_qdisc,cmd_class_0,cmd_class_1,cmd_class_2,cmd_class_3,
                      cmd_class_4,cmd_class_5]
            for i in cmd_list:
                shell(i)
                time.sleep(0.1)

    def tranffic_create_route(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            tmp = func(*args,**kwargs)
            dest_ip = tmp[0]
            port = 'eth0'
            working_time = ['9','10','11','12','13','14','15','16','17','18','19','20']
            closing_time = ['0','1','2','3','4','5','6','7','8','21','22','23']
            #current_time = str(time.localtime().tm_hour)
            current_time = tmp[1]
            if current_time in working_time:
                current_qdisc_cmd = 'tc qdisc ls dev eth0 |grep "htb 1:"'
                current_qdisc_status = shell(current_qdisc_cmd)
                current_filter_cmd = 'tc filter ls dev eth0|grep "1:4"'
                current_filter_status = shell(current_filter_cmd)
                print "current qdisc:%s curent filter:%s" % (current_qdisc_status,current_filter_status)
                if current_qdisc_status and current_filter_status:
                    print('==========working times nothing to do...============')
                    pass
                else:
                    cmd_filter_add = 'tc filter add dev eth0 parent 1:0 protocol ip prio 100 u32 \
                          match ip dst %s flowid 1:4' % dest_ip
                    cmd_filter_del = 'tc filter del dev eth0 parent 1:0 protocol ip prio 100 u32 \
                          match ip dst %s ' % dest_ip
                    cmd_list = [cmd_filter_del,cmd_filter_add]
                    for i in cmd_list:
                        shell(i)

            elif current_time in closing_time:
                current_qdisc_cmd = 'tc qdisc ls dev eth0 |grep "htb 1:"'
                current_qdisc_status = shell(current_qdisc_cmd)
                current_filter_cmd = 'tc filter ls dev eth0|grep "1:1"'
                current_filter_status = shell(current_filter_cmd)
                print "current qdisc:%s curent filter:%s" % (current_qdisc_status,current_filter_status)
                if current_qdisc_status and current_filter_status:
                    print('==========closing times nothing to do...============')
                    pass
                else:
                    cmd_filter_add = 'tc filter add dev eth0 parent 1:0 protocol ip prio 100 u32 \
                          match ip dst %s flowid 1:1' % dest_ip
                    cmd_filter_del = 'tc filter del dev eth0 parent 1:0 protocol ip prio 100 u32 \
                          match ip dst %s ' % dest_ip
                    cmd_list = [cmd_filter_del,cmd_filter_add]
                    for i in cmd_list:
                        shell(i)
            return tmp
        return wrapper





    @tranffic_create_route
    def tranffic_input(self,dest_ip,times):
        return (dest_ip,times)


if __name__ == '__main__':
    dest_ip = '172.16.201.111'
    #local_ip = '10.9.0.100'
    print('====================开始运行===============')
    print('目标ip:%s' % (dest_ip))
    print('=========================================')
    #times = str(time.localtime().tm_hour)
    action = tranffic_action()
    action.tranffic_init()
    while True:
        print('========process start ....===========================')
        times = str(time.localtime().tm_hour)
        mins = str(time.localtime().tm_min)
        action.tranffic_input(dest_ip,times)
        print('现在时间取值以小时为单位:%s分钟:%s' %(times,mins))
        print('======================================')
        time.sleep(10)
        continue

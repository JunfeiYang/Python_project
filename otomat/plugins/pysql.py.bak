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
import os,sys,time
import MySQLdb
from otomat.conf import conf


#recv_data = {'hostname': 'node1', 'swap_freed': '1839', 'cpu_idle': '0', 'cpu_user': '0', 'cpu_loadavg': ' 0.00, 0.00, 0.00', 'mem_used': '765', 'mem_total': '1877', 'networktraffic_recv_error': 0, 'swap_used_percent': '0', 'login_user_num': '6', 'swap_total': '1839', 'networktraffic_recv': 88230149, 'networktraffic_sent': 10030439, 'cpu_steal': '0', 'mem_used_percent': ['40.7565'], 'cpu_nice': '0', 'swap_used': '0', 'networktraffic_sent_error': 0, 'mem_freed': '1111', 'host_ip': '172.24.0.23', 'disk_total': 7092494336, 'mem_buffers_freed': '1758', 'disk_freed': 4906565632, 'cpu_iowait': '0', 'login_user_name': 'root root Test root root root', 'mem_buffers_used': '118', 'cpu_system': '0', 'disk_used_percent': 25.699999999999999, 'disk_used': 1825640448}

def pysql(recv_data):
    data = recv_data
    config = conf.otomat_conf('/etc/otomat/otomat.cnf')
    hostname = config.db_host()
    username = config.db_user()
    password = config.db_password()
    defdata = config.db_defaultdb()
    conn = MySQLdb.connect(host=hostname,user=username,passwd=password,db=defdata)
    cursor = conn.cursor()
    # sqltext cpu,mem,network,disk,login
    sqltext_cpu = "insert into `cpu` (Hostname,Host_ip,TIME,CPU_Loadavg,CPU_User,CPU_Nice,CPU_System,CPU_Iowait,CPU_Steal,CPU_Idel\
        ) value (\
        %s,%s,(NOW()),%s,%s,%s,%s,%s,%s,%s)"
    sqltext_mem = "insert into `mem` (Hostname,Host_ip,TIME,MEM_Total,MEM_Freed,MEM_Used,\
        MEM_Buffers_Freed,MEM_Buffers_Used,MEM_Used_Percent,SWAP_Total,SWAP_Freed,SWAP_Used,SWAP_Used_Percent\
        ) value (\
        %s,%s,(NOW()),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    sqltext_disk = "insert into `disk` (Hostname,Host_ip,TIME,DISK_Total,DISK_Used,DISK_Freed,DISK_Used_Percent\
        ) value (\
        %s,%s,(NOW()),%s,%s,%s,%s)"
    sqltext_network = "insert into `network` (Hostname,Host_ip,TIME,Networktraffic_recv,Networktraffic_recv_err,\
        Networktraffic_sent,Networktraffic_sent_err) value (\
        %s,%s,(NOW()),%s,%s,%s,%s)"
    sqltext_login = "insert into `login_user` (Hostname,Host_ip,TIME,User_num,User_name\
        ) value (\
        %s,%s,(NOW()),%s,%s)"

    #args = [('client','172.16.209.219','0.0','1036570','389505024L',
    #   '647065600L','15.300000000000001','2080370688L','2080370688L',
    #   '0L','0.0','30414569','2494730240','47665602560',
    #   '4.7000000000000002','30414569','81069')]
    hostname = data['hostname']
    hostip = data['host_ip']
    cpu_loadavg = str(data['cpu_loadavg'])
    cpu_user = str(data['cpu_user'])
    cpu_nice = str(data['cpu_nice'])
    cpu_system = str(data['cpu_system'])
    cpu_iowait = str(data['cpu_iowait'])
    cpu_steal = str(data['cpu_steal'])
    cpu_idle = str(data['cpu_idle'])
    mem_total = str(data['mem_total'])
    mem_freed = str(data['mem_freed'])
    mem_used = str(data['mem_used'])
    mem_buffers_used = str(data['mem_buffers_used'])
    mem_buffers_freed = str(data['mem_buffers_freed'])
    mem_used_percent = str(data['mem_used_percent'])
    swap_total = str(data['swap_total'])
    swap_freed = str(data['swap_freed'])
    swap_used = str(data['swap_used'])
    swap_used_percent = str(data['swap_used_percent'])
    disk_total = str(data['disk_total'])
    disk_used = str(data['disk_used'])
    disk_freed = str(data['disk_freed'])
    disk_used_percent = str(data['disk_used_percent'])
    nic_recv = str(data['networktraffic_recv'])
    nic_recv_err = str(data['networktraffic_recv_error'])
    nic_sent = str(data['networktraffic_sent'])
    nic_sent_err = str(data['networktraffic_sent_error'])
    user_name = str(data['login_user_name'])
    user_num = str(data['login_user_num'])
    ###############################
    args_cpu = (hostname,hostip,cpu_loadavg,cpu_user,cpu_nice,cpu_system,
    cpu_iowait,cpu_steal,cpu_idle)
    args_mem = (hostname,hostip,mem_total,mem_freed,mem_used,mem_buffers_used,mem_buffers_freed,mem_used_percent,swap_total,swap_freed,swap_used,swap_used_percent)
    args_disk = (hostname,hostip,disk_total,disk_used,disk_freed,disk_used_percent)
    args_network = (hostname,hostip,nic_recv,nic_recv_err,nic_sent,nic_sent_err)
    args_login = (hostname,hostip,user_num,user_name)
    ###############################
    # sqltext cpu,mem,network,disk,login
    sqltext_cpu = "insert into `cpu` (Hostname,Host_ip,TIME,CPU_Loadavg,CPU_User,CPU_Nice,CPU_System,CPU_Iowait,CPU_Steal,CPU_Idel\
        ) value (\
        %s,%s,(NOW()),%s,%s,%s,%s,%s,%s,%s)"
    sqltext_mem = "insert into `mem` (Hostname,Host_ip,Time,MEM_Total,MEM_Freed,MEM_Used,\
        MEM_Buffers_Freed,MEM_Buffers_Used,MEM_Used_Percent,SWAP_Total,SWAP_Freed,SWAP_Used,SWAP_Used_Percent\
        ) value (\
        %s,%s,(NOW()),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    sqltext_disk = "insert into `disk` (Hostname,Host_ip,TIME,DISK_Total,DISK_Used,DISK_Freed,DISK_Used_Percent\
        ) value (\
        %s,%s,(NOW()),%s,%s,%s,%s)"
    sqltext_network = "insert into `network` (Hostname,Host_ip,TIME,Networktraffic_recv,Networktraffic_recv_err,\
        Networktraffic_sent,Networktraffic_sent_err) value (\
        %s,%s,(NOW()),%s,%s,%s,%s)"
    sqltext_login = "insert into `login_user` (Hostname,Host_ip,TIME,User_num,User_name\
        ) value (\
        %s,%s,(NOW()),%s,%s)"

    #args = [('client','172.16.209.219','0.0','1036570','389505024L',
    #   '647065600L','15.300000000000001','2080370688L','2080370688L',
    #   '0L','0.0','30414569','2494730240','47665602560',
    #   '4.7000000000000002','30414569','81069')]
    hostname = data['hostname']
    hostip = data['host_ip']
    cpu_loadavg = str(data['cpu_loadavg'])
    #####################################
    # mysql.execute(sqltext,args,mode=otomat_sql.DICTCURSOR_MODE)
    cursor.execute(sqltext_cpu,args_cpu)
    cursor.execute(sqltext_mem,args_mem)
    cursor.execute(sqltext_network,args_network)
    cursor.execute(sqltext_disk,args_disk)
    cursor.execute(sqltext_login,args_login)
    cursor.close()
    conn.commit()
    conn.close()
    '''
    sqltext_dic = {sqltext_cpu:args_cpu,sqltext_mem:args_mem,sqltext_network:args_network,
                    sqltext_disk:args_disk,sqltext_login:args_login}
    for (sqltext,args) in sqltext_dic.items():
        mysql.execute(sqltext,args,mode=otomat_sql.DICTCURSOR_MODE)
        time.sleep(0.5)
    '''


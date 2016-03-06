#-*- encoding:utf-8 -*-
#!/bin/env python

import otomat_sql
'''
    report_list 这张表很简单。
    +----------------------+--------------------------------+------+-----+---------+-----------------------------+
    | Field                | Type                           | Null | Key | Default | Extra                       |
    +----------------------+--------------------------------+------+-----+---------+-----------------------------+
    | ID                   | int(11)                        | NO   | PRI | NULL    | auto_increment              |
    | HostName             | varchar(50)                    | YES  |     | NULL    |                             |
    | Host_ip              | varchar(16)                    | YES  |     | NULL    |                             |
    | Time                 | timestamp                      | YES  |     | NULL    | on update CURRENT_TIMESTAMP |
    | Cpu_Utilization      | decimal(6,2) unsigned zerofill | YES  |     | NULL    |                             |
    | Mem_total            | bigint(6)                      | YES  |     | NULL    |                             |
    | Mem_free             | bigint(6)                      | YES  |     | NULL    |                             |
    | Mem_used             | bigint(6)                      | YES  |     | NULL    |                             |
    | Mem_percent          | decimal(6,2)                   | YES  |     | NULL    |                             |
    | Swap_total           | bigint(6)                      | YES  |     | NULL    |                             |
    | Swap_free            | bigint(6)                      | YES  |     | NULL    |                             |
    | Swap_used            | bigint(6)                      | YES  |     | NULL    |                             |
    | Swap_percent         | decimal(6,2)                   | YES  |     | NULL    |                             |
    | Disk_total           | bigint(6)                      | YES  |     | NULL    |                             |
    | Disk_used            | bigint(6)                      | YES  |     | NULL    |                             |
    | Disk_free            | bigint(6)                      | YES  |     | NULL    |                             |
    | Disk_percent         | decimal(6,2)                   | YES  |     | NULL    |                             |
    | Network_traffic_recv | bigint(6)                      | YES  |     | NULL    |                             |
    | Network_traffic_sent | bigint(6)                      | YES  |     | NULL    |                             |
    +----------------------+--------------------------------+------+-----+---------+-----------------------------+
    19 rows in set (0.00 sec)

     本文主要的所有操作都针对该表。
'''
'''
def printAuthors(res,mode=0,lines=0):
        """
        格式化输出
        """
        print "*"*20, " lines: ",lines ," ","*"*20
        if mode==0  :
            for HostName in res :
                print "HostName :%s"\
                % (HostName)
        else :
            for item in res :
                print "-----------"
                for key in item.keys():
                    print key ," : ",item[key]

'''

#建立连接
mysql = otomat_sql.PyMysql()
mysql.newConnection(
        host="172.16.209.110",
        user="otomat",
        passwd="otomat",
        defaultdb="otomat")

#定义sql语句
sqltext = "select * from report_list order by ID "
#调用query方法,得到result
lines , res = mysql.query(sqltext, mode=otomat_sql.STORE_RESULT_MODE)
#提取数据
data = mysql.fetch_queryresult(res, maxrows=20, how=0, moreinfo=False)
#打印
print (data,0,lines)


#演示多行插入
sqltext = "insert into `report_list` (HostName,Host_ip,Time,Cpu_Utilization,Mem_total,Mem_free,Mem_used,Mem_percent,Swap_total,Swap_free,Swap_used,Swap_percent,Disk_total,Disk_used,Disk_free,Disk_percent,Network_traffic_recv,Network_traffic_sent) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)”"
args=['client','172.16.209.219','NOW()','0.0','1036570624L','389505024L','647065600L','15.300000000000001','2080370688L','2080370688L','0L','0.0','30414569','2494730240','47665602560','4.7000000000000002','30414569','81069']

lines ,cur = mysql.execute(sqltext,args,mode=otomat_sql.DICTCURSOR_MODE,many=True)
print "*"*20, lines ,"行被插入 ","*"*20

sqltext = "select * from report order by ID "
#调用cursor.execute方法,得到result
lines ,cur = mysql.execute(sqltext,mode=otomat_sql.DICTCURSOR_MODE)
#提取数据
data = mysql.fetch_executeresult(cur, mode=otomat_sql.FETCH_MANY, rows=20)
#打印
print (data,1,lines)


#关闭连接
mysql.closeConnnection()

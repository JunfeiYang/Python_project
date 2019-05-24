# !/usr/bin/env python
# --*-- coding:utf-8 -*-
#  Author: Andre Yang
#  Email: yangjunfei2146@gmail.com
#  File Name:
#  Description:
#  Edit History:
# ==================================================
import os,time 
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

import cx_Oracle

user="c##fsz"
passwd="123456"
co="172.16.1.222:1521/CRMLIMS"


def show_tables(sql):
    conn=cx_Oracle.connect(user,passwd,co,encoding = "UTF-8", nencoding = "UTF-8")
    curs=conn.cursor()
    print "show: %s" %sql
    #sql='select * from fsz_users where id=1'
    #sql='select * from fsz_users'
    try:
        #curs.execute(sql)
        rr=curs.execute(sql)
        result=rr.fetchall()
        #print "查询内容：%s" %result
        sql_list = []
        for i in range(0,len(result[0])):
         print result[0][i],
    except cx_Oracle.DatabaseError as e:
        error = e.args
        print "Oracle-Error-Code: %s" %error.code
        print "Oracle-Error-Message: %s" %error.message    
    curs.close()
    conn.close()
def insert_data(sql):
    conn=cx_Oracle.connect(user,passwd,co,encoding = "UTF-8", nencoding = "UTF-8")
    curs=conn.cursor()
    print sql
    try:
        curs.execute(sql)
        curs.execute("commit")
        print "数据插入成功"
    except cx_Oracle.DatabaseError as exc:
        error = exc.args
        print "Oracle-Error-Code: %s" %error.code
        print "Oracle-Error-Message: %s"  %error.message    
        print "数据插入失败" 
    curs.close()
    conn.close()
 


if __name__ == '__main__':
    # sql="INSERT INTO fsz_users VALUES(name,age,gender,height,brithdate,address);"
    for x in list(xrange(0,92233720)):
        insert_sql="insert into fsz_users  values (%s,'alex',8,'男',118,to_date('2011-12-01','YYYY-MM-DD'),'北京市东城区')" %x
        select_sql="select * from fsz_users where id=%s" %x
        insert_data(insert_sql)
        time.sleep(1)
        print "======"
        show_tables(select_sql)
        print "#######"
        time.sleep(60)


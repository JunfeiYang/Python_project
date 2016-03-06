#coding=gbk

##############################################################
# Copyright (C), 2009-2010, aliyun
# FileName: dbunit.py
# Author: elbert.chenh
# Version: 0.1
# History:
# <Author/Maintainer> <Date> <Modification>
# elbert.chenh 10/07/11 Create this file
#############################################################
import sys
import ConfigParser
import datetime,time
import binascii
import os
import types
import os
import pdb
import pymssql

class DBUnit:
def __init__(self,user=None,passwd=None,host=None,database=None):
try:
self.connection = pymssql.connect(host=host, user = user, password =passwd, database=database)
self.cursor= self.connection.cursor()
except:
print "Could not connect to DB server."
exit(0)




def __del__(self):
self.cursor.close()
self.connection.close()

def read(self,Sql,param=None):
'''Exec select sql , return type is Tuple,use len fun return select row num
use param like this:
Sql=select * from table where param=%s and param1=%s
param=(value1,valuei2)
'''
try:
cursor = self.connection.cursor()
if param==None:
cursor.execute(Sql)
rs = cursor.fetchall()
cursor.close()
else:
cursor.execute(Sql,param)
rs = cursor.fetchall()
cursor.close()
except Exception,e:
print e
rs = ()
return rs

def write(self,sql,param,iscommit=True):
try:
cursor = self.connection.cursor()
print sql
n = cursor.executemany(sql,param)
if iscommit :
self.connection.commit()
return n
except Exception,e:
print e
self.connection.rollback()
return -1
def writeOneRecord(self,sql):
try:
cursor = self.connection.cursor()
n = cursor.execute(sql)
self.connection.commit()
return int(cursor.lastrowid)
except:
self.connection.rollback()
return -1



if __name__ == '__main__':
a = time.time()
db = DBUnit('accelbert08','a1234561','cacelbert01.mysql.alibabalabs.com:3306','elbert08') 
rs = db.read("select count(*) from t_file")
print rs
#db.delete(dictinu)
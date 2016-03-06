#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import MySQLdb
import MySQLdb.cursors

STORE_RESULT_MODE = 0
USE_RESULT_MODE = 1
#
CURSOR_MODE = 0
DICTCURSOR_MODE = 1
SSCURSOR_MODE = 2
SSDICTCURSOR_MODE =3
#
FETCH_ONE = 0
FETCH_MANY = 1
FETCH_ALL = 2

#connection
class PyMysql:
	def __init__(self):
		self.conn = None
		pass
	def newConnection(self,host,user,passwd,defaultdb):
		"""
		Establish a new connection, designated host, user name, password, default database
		"""
		self.conn = MySQLdb.Connect(host,user,passwd,defaultdb)
		if self.conn.open == False:
			raise None
	def closeConnection(self):
		"""
		Close the current connection
		"""
		self.conn.close()
	def query(self,sqltext,mode=STORE_RESULT_MODE):
		"""
		作用：使用connection对象的query方法，并返回一个元组(影响行数(int),结果集(result))
        	参数：sqltext：sql语句
            	     mode=STORE_RESULT_MODE（0） 表示返回store_result，mode=USESTORE_RESULT_MODE（1） 表示返回use_result
       		返回：元组(影响行数(int),结果集(result)
       		"""
       		if self.conn == None or self.conn.open == False:
       		 	return -1
       		self.conn.query(sqltext)
       		if mode == 0:
       		 	result = self.conn.store_result()
       		elif mode == 1:
       		 	result = self.conn.use_result()
       		else:
       		 	raise Exception("mode value is wrong.")
       		return (self.conn.affected_rows(),result)
       	def fetch_queryresult(self,result,maxrows=1,how=0,moreinfo=False):
       		"""
       		参数:result： query后的结果集合
            		        maxrows： 返回的最大行数
            		        how： 以何种方式存储结果
             			(0：tuple,1：dictionaries with columnname,2：dictionaries with table.columnname)
            			moreinfo 表示是否获取更多额外信息（num_fields，num_rows,num_fields）
        	返回：元组（数据集，附加信息（当moreinfo=False）或单一数据集（当moreinfo=True）
        	"""
		if result == None:
        			return None
		dataset = result.fetch_row(maxrows,how)
		if moreinfo is False:
        			return dataset
		else:
        			num_fields = result.num_fields()
        			num_rows = result.num_rows()
        			filed_flags = result.field_flags()
        			info = (num_fields,num_rows,field_flags)
        			return (dataset,info)
        def execute(self,sqltext,args=None,mode=CURSOR_MODE,many=False):
        	"""
        	作用：使用游标（cursor）的execute 执行query
        	参数：  sqltext： 表示sql语句
             		rgs： sqltext的参数
             		mode：以何种方式返回数据集
                	    CURSOR_MODE = 0 ：store_result , tuple
                	    DICTCURSOR_MODE = 1 ： store_result , dict
                	    SSCURSOR_MODE = 2 : use_result , tuple
                	    SSDICTCURSOR_MODE = 3 : use_result , dict
            		many：是否执行多行操作（executemany）
        	返回：元组（影响行数（int），游标（Cursor））
        	"""
        	if mode == CURSOR_MODE:
        	    curclass = MySQLdb.cursors.Cursor
        	elif mode == DICTCURSOR_MODE:
        	    curclass = MySQLdb.cursors.DictCursor
        	elif mode == SSCURSOR_MODE:
        	    curclass = MySQLdb.cursors.SSCursor
        	elif mode == SSDICTCURSOR_MODE:
        	    curclass = MySQLdb.cursors.SSDictCursor
        	else:
        	    raise Exception("mode value is wrong")

        	cur = self.conn.cursor(cursorclass = curclass)
        	line = 0
        	if many == False:
        	    if args == None:
        		line = cur.execute(sqltext)
        	    else:
        		line = cur.executemany(sqltext,args)
        	else:
        		if args == None:
        		    line = cur.executemany(sqltext)
                	else:
        		    line = cur.executemany(sqltext,args)
        	return (line,cur)
        def fetch_executeresult(self,cursor,mode=FETCH_ONE,rows=1):
                """
        	    作用：提取cursor获取的数据集
        	    参数：  cursor：游标
             			mode：执行提取模式
              		        FETCH_ONE: 提取一个；
                                FETCH_MANY :提取rows个 ；
                                FETCH_ALL : 提取所有
             			rows：提取行数
       		    返回：fetch数据集
       		"""
       		if cursor == None:
       		    return
       		if mode == FETCH_ONE:
       		    return cursor.fetchone()
       		elif mode == FETCH_MANY:
       		    return cursor.fetchmay(rows)
       		elif mode == FETCH_ALL:
       		    return cursor.fetchall()

if __name__ == "__main__":
	print help(PyMysql)


import MySQLdb

con = MySQLdb.connect('localhost','rain','che001','online')
curl = con.cursor()
curl.execute("select * from online_user")
'''
rows = curl.fetchall()
for row in rows:
	print row
'''
rows = int(curl.rowcount)
for i in range(rows):
	row = curl.fetchone()
	print row[0],row[1],row[2]

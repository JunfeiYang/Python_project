
import MySQLdb

con = MySQLdb.connect('localhost','rain','che001','online')
curl = con.cursor()
curl.execute("select * from online_user")
rows = curl.fetchall()
desc = curl.description
print 'The description is',desc
print "%s,%s,%s" % (desc[0][0],desc[1][0],desc[2][0])
'''
for row in rows:
	print row 
data = int(curl.rowcount)
for i in range(data):
        row = curl.fetchone()
        print row[0],row[1],row[2]
'''

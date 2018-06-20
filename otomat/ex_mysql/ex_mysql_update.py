
import MySQLdb

con = MySQLdb.connect('localhost','rain','xxx001','online')
with con:p
	curl = con.cursor()
	curl.execute("update Writers SET Name=%s where Id=%s",("Yangjunfei","5"))
	print "Number of rows updated:%d" % curl.rowcount
	curl.close()
con.close()

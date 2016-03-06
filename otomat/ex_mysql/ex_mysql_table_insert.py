
import MySQLdb

con = MySQLdb.connect('localhost','rain','che001','online')
with con:
	curl = con.cursor()
	curl.execute("CREATE TABLE IF NOT EXISTS author(Id INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(25))")
    	curl.execute("INSERT INTO author(Name) VALUES('Rain Wang')")
    	curl.execute("INSERT INTO author(Name) VALUES('Andre Yang')")
    	curl.execute("INSERT INTO author(Name) VALUES('Carlos Hu')")
	curl.close()
con.close()

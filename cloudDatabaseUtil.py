import mysql.connector

def loginReader(username, password):
	cnx = mysql.connector.connect(user='sd2810', password='26842810',
                              host='cs4111.cf7twhrk80xs.us-west-2.rds.amazonaws.com',
                              database='bigdata')
	cursor = cnx.cursor()
	query = ("SELECT * FROM `reader` where username = %s and password = %s")
	cursor.execute(query, (username, password))
	res = cursor.fetchone()
	cnx.close()
	if res:
		return True
	else:
		return False

def registerReader(username, password):
	cnx = mysql.connector.connect(user='sd2810', password='26842810',
                              host='cs4111.cf7twhrk80xs.us-west-2.rds.amazonaws.com',
                              database='bigdata')
	cursor = cnx.cursor()
	query = ("INSERT INTO `reader` (username, password) VALUES (%s, %s)")
	try:
		cursor.execute(query, (username, password))
	 	cnx.commit()
	 	cnx.close()
	 	return True
	except:
	 	cnx.close()
	 	return False

def rateBook(username, bookid, rate):
	cnx = mysql.connector.connect(user='sd2810', password='26842810',
                              host='cs4111.cf7twhrk80xs.us-west-2.rds.amazonaws.com',
                              database='bigdata')
	cursor = cnx.cursor()
	query = ("INSERT INTO `rate` (username, bookid, rate) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE rate = %s")
	try:
		cursor.execute(query, (username, bookid, rate, rate))
	 	cnx.commit()
	 	cnx.close()
	 	return True
	except:
	 	cnx.close()
	 	return False

def getRating(username):
	cnx = mysql.connector.connect(user='sd2810', password='26842810',
                              host='cs4111.cf7twhrk80xs.us-west-2.rds.amazonaws.com',
                              database='bigdata')
	cursor = cnx.cursor()
	query = ("SELECT bookid, rate FROM `rate` where username = %s")
	cursor.execute(query, (username))
	res=[]
	for (bookid, rate) in cursor:
		res.append((0,bookid,rate))
	cnx.close()
	return res

if __name__ == "__main__":
	print getRating("a")
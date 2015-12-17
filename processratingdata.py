'''This program map old rating (ISBN) to new rating (bookid)'''
import mysql.connector

cnx = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='bigdata')

cursor = cnx.cursor()

query = ("SELECT `User-ID`, `ISBN`, `Book-Rating` FROM `BX-Book-Ratings`")

add_book = ("INSERT INTO rate "
               "(userid, bookid, rate) "
               "VALUES (%s, %s, %s)")

anothercnx = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='bigdata')
anothercursor = anothercnx.cursor()

thirdcnx = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='bigdata')
thirdcursor = thirdcnx.cursor()
thrirdquery=("SELECT bookid from book where ISBN = %s ")

cursor.execute(query)

for (User_ID, ISBN, Book_Rating) in cursor:
	thirdcursor.execute(thrirdquery,(ISBN,))
	bookid = thirdcursor.fetchone()
	if bookid:
		book = (User_ID, bookid[0], Book_Rating)
		anothercursor.execute(add_book, book)

anothercnx.commit()
anothercnx.close()
thirdcnx.close()
cnx.close()
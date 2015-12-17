'''this file add a bookid to book, so it can be used by spark ALS'''
import mysql.connector

cnx = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='bigdata')

cursor = cnx.cursor()

query = ("SELECT `ISBN`, `Book-Title`, `Book-Author`, `Publisher`, `Image-URL-S`, `Image-URL-M`, `Image-URL-L` FROM `BX-Books`")

add_book = ("INSERT INTO book "
               "(ISBN, title, author, publisher, images, imagem, imagel) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)")

anothercnx = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='bigdata')
anothercursor = anothercnx.cursor()

cursor.execute(query)

for (ISBN, Book_Title, Book_Author, Publisher, Image_URL_S, Image_URL_M, Image_URL_L) in cursor:
	book = (ISBN, Book_Title, Book_Author, Publisher, Image_URL_S, Image_URL_M, Image_URL_L)
	anothercursor.execute(add_book, book)

anothercnx.commit()
anothercnx.close()
cnx.close()
# for data parser only
drop table if exists reader;
drop table if exists rate;
drop table if exists book;
 
CREATE TABLE reader (
	username char NOT NULL,
	password char NOT NULL,
	PRIMARY KEY(username)
)	ENGINE=INNODB;

CREATE TABLE book (
    bookid Int(10) Not Null Auto_Increment,
	ISBN char(13),
	title char(255),
	author char(255),
	publisher char(255),
	images char(255),
	imagem char(255),
	imagel char(255),
    PRIMARY KEY(bookid)
)   ENGINE=INNODB;

CREATE TABLE rate (
    userid int NOT NULL,
	bookid int NOT NULL,
	rate float,
    PRIMARY KEY(userid, bookid),
    FOREIGN KEY (bookid)
      REFERENCES book(bookid)
)	ENGINE=INNODB;


CREATE TABLE `BX-Books` (
  `ISBN` varchar(13) binary NOT NULL default '',
  `Book-Title` varchar(255) binary default NULL,
  `Book-Author` varchar(255) binary default NULL,
  `Year-Of-Publication` int(10) unsigned default NULL,
  `Publisher` varchar(255) binary default NULL,
  `Image-URL-S` varchar(255) binary default NULL,
  `Image-URL-M` varchar(255) binary default NULL,
  `Image-URL-L` varchar(255) binary default NULL,
  PRIMARY KEY  (`ISBN`)
) ENGINE=MyISAM;


SELECT bookid,title,author,publisher,images,imagem,imagel FROM rate where userid < 1000 INTO OUTFILE '~/Documents/books.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';


# for cloud database
drop table if exists rate;
 drop table if exists reader;

CREATE TABLE reader (
	username char NOT NULL,
	password char NOT NULL,
	PRIMARY KEY(username)
)	ENGINE=INNODB;

CREATE TABLE rate (
    username char NOT NULL,
	bookid int NOT NULL,
	rate float,
    PRIMARY KEY(username, bookid),
    FOREIGN KEY (username)
      REFERENCES reader(username)
)	ENGINE=INNODB;
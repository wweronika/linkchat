CREATE TABLE Users (
	ID integer PRIMARY KEY AUTOINCREMENT,
	login string,
	password string,
	salt string,
	email string 
);

CREATE TABLE Messages (
	ID integer PRIMARY KEY AUTOINCREMENT,
	senderID integer,
	isLink boolean,
	groupID integer,
	text string
);

CREATE TABLE Groups (
	ID integer PRIMARY KEY AUTOINCREMENT,
	name string
);

CREATE TABLE Links (
	ID integer PRIMARY KEY AUTOINCREMENT,
	messageID integer
);

CREATE TABLE group_user (
	groupID integer,
	userID integer
);

CREATE TABLE Tokens (
	User_ID integer,
	token string,
	token_data string
);


/*

	Import some users

*/

INSERT INTO Users (login, password, salt, email) values("wint3rmute","111","111","mateusz.baczek1998@gmail.com");
INSERT INTO Users (login, password, salt, email) values("wweronika","111","111","weronika@aaa.com");
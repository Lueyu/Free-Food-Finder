/*
 messages table
 messageid, integer, primary key
 sender, at most 20 chars, foreign key to users
 receiver, at most 20 chars, foreign key to users
 created, DATETIME type, automatically set by SQL engine to current date/time
 filename, at most 64 chars
 message, Text field max 2GB 
 */
CREATE TABLE info(
    foodID integer primary key autoincrement,
    uniqname VARCHAR(20) NOT NULL,
    campus VARCHAR(30) NOT NULL,
    locName VARCHAR(200) NOT NULL,
    lat REAL,
    lng REAL,
    foodType VARCHAR(20) NOT NULL,
    foodDate VARCHAR(50) NOT NULL,
    requirement VARCHAR(2000),
    organization VARCHAR(200)
);

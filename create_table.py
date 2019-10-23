import mysql.connector

import logging

logger = logging.getLogger("sample-logger")

Tables={}
Tables['Academic Journal'] = "CREATE TABLE Academic_Journal (Journal_Id INTEGER NOT NULL, Journal_Name CHAR(255), Category VARCHAR(255), PRIMARY KEY(Journal_Id));"

Tables['Academic Paper'] = "CREATE TABLE Academic_Paper (Paper_Id INTEGER NOT NULL, Authors CHAR(64), Journal_Id INTEGER NOT NULL, Title CHAR(255), Abstract TEXT, PRIMARY KEY(Paper_Id), FOREIGN KEY(Journal_Id) REFERENCES Academic_Journal(Journal_Id));"

Tables['Topics per Paper'] = "CREATE TABLE Topics_per_Paper (Paper_Id INTEGER NOT NULL, Topic1 INTEGER, Topic2 INTEGER, Topic3 INTEGER, Topic4 INTEGER, Topic5 INTEGER, FOREIGN KEY(Paper_Id) REFERENCES Academic_Paper(Paper_Id));"

logger.info("Connecting to SQL...")
cnx = mysql.connector.connect(user="user-411",
                              password="pass",
                              host="127.0.0.1",
                              database="testdb1")

logger.info("Creating Cursor...")
cursor=cnx.cursor()

for i in Tables:
    cursor.execute(Tables[i])
    logger.info("Inserted TABLE {0}".format(i))

cursor.close()
cnx.close()


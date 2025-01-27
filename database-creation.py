import mysql.connector

'''
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "lasya@23#"
)

print(mydb)
mycursor = mydb.cursor()

#creating a database
#mycursor.execute("CREATE DATABASE mywebsitedata")

mycursor.execute("SHOW DATABASES")

for x in mycursor:
    print(x)
'''

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "lasya@23#",
    database = "mywebsitedata"
)

mycursor = mydb.cursor()

create_table_query = """
CREATE TABLE UserCred (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    EmailID VARCHAR(255) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    ConfirmPassword VARCHAR(255) NOT NULL,
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

view_table = """
SELECT * FROM UserCred;
"""

#mycursor.execute(create_table_query)

mycursor.execute(view_table)
for x in mycursor:
    print(x)
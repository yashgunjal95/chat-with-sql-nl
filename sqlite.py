import sqlite3

## connection with sqlite
connection = sqlite3.connect('student.db')

## create a cursor to object to insert record and create table
cursor = connection.cursor()

table_info = """
CREATE TABLE STUDENTS (name VARCHAR(25), class VARCHAR(25), section VARCHAR(25), marks INT)
"""

cursor.execute(table_info)

## Insert some records

cursor.execute("""INSERT INTO STUDENTS VALUES ("yash", "data science", 'A','90')""")
cursor.execute("""INSERT INTO STUDENTS VALUES ("aarya", "ML", 'B','80')""")
cursor.execute("""INSERT INTO STUDENTS VALUES ("ubaid", "DBMS", 'C','72')""")
cursor.execute("""INSERT INTO STUDENTS VALUES ("Prashant", "cloudComp", 'A','82')""")
cursor.execute("""INSERT INTO STUDENTS VALUES ("sahil", "DAA", 'B','75')""")

### Display all the records
print("The inserted records are : ")
data = cursor.execute('SELECT * FROM Students')
for row in data:
    print(row)

##commit changes in db
connection.commit()
connection.close()
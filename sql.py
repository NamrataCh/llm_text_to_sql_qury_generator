import sqlite3

connection=sqlite3.connect("student.db")

# create a cursor object to insert record
cursor=connection.cursor()

table_info="""
create table Student(name varchar(25), class varchar(25), section varchar(25), marks int)

"""
#create table
cursor.execute(table_info)

#insert record
cursor.execute(''' insert into student values('Namrata', 'Data Science', 'A', 90)''')
cursor.execute(''' insert into student values('Daksh', 'Data Science', 'B', 80)''')
cursor.execute(''' insert into student values('Avadhut', 'Devops', 'A', 70)''')
cursor.execute(''' insert into student values('Shreeja', 'Devops', 'B', 86)''')


print("Total records are")

data=cursor.execute('''select * from student''')
for row in data:
    print(row)


# close the connection
connection.commit()
connection.close()
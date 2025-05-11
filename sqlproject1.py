import mysql.connector

con=mysql.connector.connect(user="root",password="",database="atm")
print("Connected")

cur=con.cursor()

cur.execute("create table reg (accno int(255), accholder varchar(255), balance int(4))")
con.commit()
con.close()

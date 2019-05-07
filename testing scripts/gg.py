import sqlite3
conn = sqlite3.connect("med.db")
c=conn.cursor()
y="SELECT * from record where admitted='Y'" 
x = c.execute(y)
print(x)
for row in x:
	print(row[0])
	print(row[1])
	print(row[2])
	print(row[3])
	print(row[4])
	print(row[12])
	print('aaaaaaaaaaaaaaa')
conn.commit()
conn.close()

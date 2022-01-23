import sqlite3
conn = sqlite3.connect('auto.db')
cursor = conn.execute("SELECT * from auto")
print(cursor.fetchall())
conn.close()
import sys
import sqlite3 as sql

conn = sql.connect("data.db")

with conn:
	cursor = conn.cursor()
	cursor.execute("DROP TABLE dht11data")
conn.close()

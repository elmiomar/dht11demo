import sys
import sqlite3 as sql

conn = sql.connect('data.db')

with conn:
	cursor = conn.cursor()
	cursor.execute("DROP TABLE IF EXISTS dht11data")
	cursor.execute("CREATE TABLE dht11data(timestamp DATETIME, temperature NUMERIC, humidity NUMERIC)")
conn.close()

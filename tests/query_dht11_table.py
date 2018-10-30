import sys
import sqlite3 as sql

conn = sql.connect("data_test.db")
cursor = conn.cursor()

MAX_TEMPERATURE = 30

print("\nTotal number of entries: " + str(len(cursor.execute("SELECT * FROM dht11data").fetchall())) + "\n")

print("\nQuery all DHT11DATA table content:\n")
for row in cursor.execute("SELECT * FROM dht11data"):
	print(row)

print("\nQuery entries where humdity = 33:\n")
for row in cursor.execute("SELECT * FROM dht11data WHERE humidity='33'"):
	print(row)

print("\nQuery all entries where the temperature is below 30:")
for row in cursor.execute("SELECT * FROM dht11data WHERE temperature<(?)", (MAX_TEMPERATURE,)):
	print(row)

print("\nLast entry logged:\n")
for row in cursor.execute("SELECT * FROM dht11data ORDER BY timestamp DESC LIMIT 1"):
	print(row)

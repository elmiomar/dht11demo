#! /usr/bin/python3

from flask import Flask, render_template, request
app = Flask(__name__)

import sqlite3 as sql


HOST = '0.0.0.0'
PORT = 80

# Get data from the database
def get_data():
	conn = sql.connect("../db/data.db")
	cursor = conn.cursor()
	for row in cursor.execute("SELECT * FROM dht11data ORDER BY timestamp DESC LIMIT 1"):
		timestamp = str(row[0])
		temperature = row[1]
		humidity = row[2]
	conn.close()
	return timestamp, temperature, humidity 

# Index route
@app.route("/")
def index():
	timestamp, temperature, humidity = get_data()
	data = {
		'timestamp': timestamp,
		'temperature': temperature,
		'humidity':humidity
	}
	return render_template('index.html', **data)


if __name__ == "__main__":
	app.run(debug=True, host=HOST, port=PORT)

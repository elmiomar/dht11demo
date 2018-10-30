#! /usr/bin/python3
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

from flask import Flask, render_template, make_response, request
app = Flask(__name__)

import sqlite3 as sql


DB_PATH = '../db/data.db'
HOST = '0.0.0.0'
HTTP_PORT = 80
HTTPS_PORT = 443
CERT_FILE = 'cert/cert.pem'
PRIV_KEY = 'cert/key.pem'

# Get data from the database
def get_data():
	conn = sql.connect(DB_PATH)
	cursor = conn.cursor()
	for row in cursor.execute("SELECT * FROM dht11data ORDER BY timestamp DESC LIMIT 1"):
		timestamp = str(row[0])
		temperature = row[1]
		humidity = row[2]
	conn.close()
	return timestamp, temperature, humidity 

# Store the data in the database
def log_data(humidity, temperature):
	conn = sql.connect(DB_PATH)
	cursor = conn.cursor()
	cursor.execute("INSERT INTO dht11data VALUES(datetime('now'), (?), (?))", (temperature, humidity))
	conn.commit()
	conn.close()

# Get last piece of data stored in the database
def get_last_data():
	conn = sql.connect(DB_PATH)
	cursor = conn.cursor()
	for row in cursor.execute("SELECT * FROM dht11data ORDER BY timestamp DESC LIMIT 1"):
		timestamp = str(row[0])
		temperature = row[1]
		humidity = row[2]
	conn.close()
	return timestamp, temperature, humidity 


def get_hist_data(number_samples):
	conn = sql.connect(DB_PATH)
	cursor = conn.cursor()
	data = cursor.execute("SELECT * FROM dht11data ORDER BY timestamp DESC LIMIT " + str(number_samples)).fetchall()
	timestamps = []
	temperatures = []
	humidities = []
	
	for row in reversed(data):
		timestamps.append(row[0])
		temperatures.append(row[1])
		humidities.append(row[2])
	conn.close()
	
	return  timestamps, temperatures, humidities

def max_rows_table():
	conn = sql.connect(DB_PATH)
	cursor = conn.cursor()
	for row in cursor.execute("SELECT COUNT(temperature) FROM dht11data"):	
		max_rows = row[0]
	return max_rows


global num_of_sample
num_of_sample = max_rows_table()
if num_of_sample > 101:
	num_of_sample = 100


# Index route
@app.route("/")
def index():
	timestamp, temperature, humidity = get_last_data()
	data = {
		'timestamp': timestamp,
		'temperature': temperature,
		'humidity':humidity,
		'numSamples': num_of_sample
	}
	return render_template('index.html', **data)


@app.route("/", methods=["POST"])
def form_post():
	global num_of_sample
	num_of_sample = int(request.form['numSamples'])
	num_max_samples = max_rows_table()
	if (num_of_sample > num_max_samples):
		num_of_sample = num_max_samples - 1
		
	timestamp, temperature, humidity = get_last_data()
	data = {
		'timestamp': timestamp,
		'temperature': temperature,
		'humidity':humidity,
		'numSamples': num_of_sample
	}
	return render_template('index.html', **data)


@app.route("/plots/temperature")
def plot_temperature():
	timestamps, temperatures, humidities = get_hist_data(num_of_sample)
	ys = temperatures
	figure = Figure()
	axis = figure.add_subplot(1, 1, 1)
	axis.set_title("Temperature [°C]")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(num_of_sample)
	axis.plot(xs ,ys)
	canvas = FigureCanvas(figure)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response


@app.route("/plots/humidity")
def plot_humidity():
	timestamps, temperatures, humidities = get_hist_data(num_of_sample)
	ys = humidities
	figure = Figure()
	axis = figure.add_subplot(1, 1, 1)
	axis.set_title("Humidity [%]")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(num_of_sample)
	axis.plot(xs ,ys)
	canvas = FigureCanvas(figure)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response


# DHT11 POST endpoint, handles the post requets from the sensor 
@app.route("/dht11", methods=["POST"])
def dht11_post():
	payload = request.get_json()
	temperature = payload['temperature']
	humidity = payload['humidity']
	# store data
	log_data(humidity, temperature)
	print('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))
	return 'OK'

if __name__ == "__main__":
	app.run(ssl_context=(CERT_FILE, PRIV_KEY), debug=True, host=HOST, port=HTTPS_PORT)

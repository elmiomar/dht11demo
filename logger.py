import sys
import time
import sqlite3 as sql
import Adafruit_DHT

DB_NAME = "db/data.db"
SLEEP_TIME = 2 # in seconds
FREQUENCY = 1 # in seconds (every 1 minute)
DHT11_SENSOR = Adafruit_DHT.DHT11
DHT11_SENSOR_PIN = 4


def get_data():
	humidity, temperature = Adafruit_DHT.read_retry(DHT11_SENSOR, DHT11_SENSOR_PIN)
	if humidity is not None and temperature is not None:
		humidity = round(humidity)
		temperature = round(temperature,1)
	return humidity, temperature


def log_data(humidity, temperature):
	conn = sql.connect(DB_NAME)
	cursor = conn.cursor()
	cursor.execute("INSERT INTO dht11data VALUES(datetime('now'), (?), (?))", (temperature, humidity))
	conn.commit()
	conn.close()


def main():
	while True:
		h, t = get_data()
		log_data(h, t)
		time.sleep(FREQUENCY)

main()


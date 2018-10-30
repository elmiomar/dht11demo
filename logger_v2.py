import sys
import time
import sqlite3 as sql
import Adafruit_DHT
import json
import requests

FREQUENCY = 1 # in seconds (every 1 second)
DHT11_SENSOR = Adafruit_DHT.DHT11
DHT11_SENSOR_PIN = 4
HOST = '0.0.0.0'
PORT = 443
ENDPOINT = 'dht11'


def get_data():
	humidity, temperature = Adafruit_DHT.read_retry(DHT11_SENSOR, DHT11_SENSOR_PIN)
	if humidity is not None and temperature is not None:
		humidity = round(humidity)
		temperature = round(temperature,1)
	return humidity, temperature


def send_data(humidity, temperature):
	data = {'humidity': humidity,'temperature': temperature}
	r = requests.post('https://' + HOST + ':' + str(PORT) + '/' + ENDPOINT, json=data, verify=False) # verify=False to avoid SSLCertificate error

def main():
	while True:
		humidity, temperature = get_data()
		send_data(humidity, temperature)
		time.sleep(FREQUENCY)

main()


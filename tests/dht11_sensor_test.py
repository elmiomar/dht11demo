#! /usr/bin/python3

import sys
import time
import Adafruit_DHT

dht11_sensor = Adafruit_DHT.DHT11
dht11_sensor_pin = 4

while True:
	humidity, temperature = Adafruit_DHT.read_retry(dht11_sensor, dht11_sensor_pin)

	if humidity is not None and temperature is not None:
		print('Temperature={0:0.1f}C, and Humidity={1:0.1f}%'.format(temperature,humidity))
	else:
		print('Failed to read from sensor DHT11.')
	time.sleep(2)

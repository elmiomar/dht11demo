#!/bin/bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert/cert.pem -keyout cert/key.pem -days 365

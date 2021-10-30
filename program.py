import sys
import Adafruit_DHT as dht
import RPi.GPIO as GPIO
from flask import Flask, jsonify, request
#from flask import jsonify

app = Flask(__name__)

@app.route('/')
def index():
	sensor = dht.DHT22
	pin = 4
	humidity, temperature = dht.read_retry(sensor, pin)
	print('Temp={0:0.1f} *C, Hum={1:0.1f} %'.format(temperature, humidity))
	return jsonify(Temp=temperature, Hum=humidity)

@app.route('/rele', methods=['POST'])
def turnOnRele():
    body = request.get_json()
    command = body.get('command', '')
    print(body.get('command', ''))
    pin = 15
    rele_status = 'Rele OFF'
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    if(command == 'Activate'):
        GPIO.output(pin, False)
        print('Rele ON')
        rele_status = "Rele ON"
    else:
        GPIO.output(pin, True)
        print('Rele OFF')
        GPIO.cleanup()

    return rele_status

if __name__=='__main__':
	app.run(debug=True, host='0.0.0.0')

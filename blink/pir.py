import RPi.GPIO as GPIO
import time
import requests
import os

HA_HOST = os.environ.get('HA_HOST')
HA_TOKEN = os.environ.get('HA_TOKEN')

HTTP_BASE = 'http://{}'.format(HA_HOST)

url = '{}/api/events/bathroom_motion'.format(HTTP_BASE)
headers = {
    "Authorization": "Bearer {}".format(HA_TOKEN),
    "content-type": "application/json",
}

pir_sensor = 11
piezo = 7

GPIO.setmode(GPIO.BOARD)

GPIO.setup(piezo,GPIO.OUT)

GPIO.setup(pir_sensor, GPIO.IN)

current_state = 0
try:
    while True:
		time.sleep(0.01)
		current_state = GPIO.input(pir_sensor)
		if current_state == 1:
			resp = requests.post(url, headers=headers)
			print(resp)
			print("GPIO pin %s is %s" % (pir_sensor, current_state))
			GPIO.output(piezo,True)
			time.sleep(1)
			GPIO.output(piezo,False)
except KeyboardInterrupt:
	pass
finally:
	GPIO.cleanup()

import time
import binascii
import machine
from mqtt import MQTTClient
from machine import Pin
import os, sys

# Many ESP8266 boards have active-low "flash" button on GPIO0.
# Here use Pico W Pin 14
button = Pin(14, Pin.IN, Pin.PULL_DOWN)

random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

ADAFRUIT_IO_URL = b'io.adafruit.com' 
ADAFRUIT_USERNAME = b'profhuster'
ADAFRUIT_IO_KEY = b'aio_GTyf844q6RWzHSdW5vG7SPiQDo7i'
ADAFRUIT_IO_FEEDNAME = b'testButton'

client = MQTTClient(client_id=mqtt_client_id, 
                    server=ADAFRUIT_IO_URL, 
                    user=ADAFRUIT_USERNAME, 
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)

try:            
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()

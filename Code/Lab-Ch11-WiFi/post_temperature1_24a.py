""" post_temperature1 - Posts CPU temerature to io.adafruit.com. """


from connect import wlan, settings
from time import sleep_ms
from binascii import hexlify
from random import randint
from umqtt.simple import MQTTClient
from machine import Pin, unique_id

print("\n==== post_temperature1 ====\n")

aio_username = settings['ADAFRUIT_AIO_USERNAME']
aio_key = settings['ADAFRUIT_AIO_KEY']
# This feed name will show up on your io.adafruit.com page Feeds
aio_feed_name = "test-1"

# Default MQTT server to connect to
SERVER = settings['ADAFRUIT_SERVER']
CLIENT_ID = hexlify(machine.unique_id())[-4:]
# The topic of the mqtt message
mqtt_topic = aio_username + "/feeds/" + aio_feed_name 

####

def main(server=SERVER):
    c = MQTTClient(CLIENT_ID, SERVER, port=1883, user=aio_username, password=aio_key, \
           keepalive=300, ssl=False)
    c.connect()
    print(f"Connected to {server}")
    try:
        while True:
            temp = str(randint(200, 300)/10)
            print(f"Publishing {temp}")
            c.publish(mqtt_topic, temp)
            sleep_ms(5000)
    except:
        print("Exception. Disconnecting")
        c.disconnect()

main()
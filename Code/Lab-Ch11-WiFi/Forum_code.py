""" From https://forums.adafruit.com/viewtopic.php?p=1010015&hilit=mqtt+micropython#p1010015 """

import machine, time, network
from mqtt import MQTTClient
from random import randint

# CONFIGURE THESE VARIABLES::                                                          
wifi_ssid = "Ruthless" # The name of your wifi network
wifi_password = "Georgeless" # The wifi password

aio_username = "astrohuster" # The adafruit io username
aio_api_key = "aio_TfqB88sgsanYJ69FWBWBbq9DDfBY" # The adafruit io api key
aio_feed_name = "test-feed" # The name of the adafruit io feed

mqtt_device_id = "test-device" # The name of the device for MQTT



# DON'T CONFIGURE THESE VARIABLES
mqtt_topic = aio_username + "/feeds/" + aio_feed_name # The topic of the mqtt message


# Network:
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# This function connects the board to wifi.
# The led slowly blinks while waiting for a connection:
def connect_wlan():
    global wlan
    print("Connecting .", end='')
    wlan.connect(wifi_ssid, wifi_password)
    while True:
        print(".", end='')
        if wlan.isconnected():
            break
        if wlan.status() != network.STAT_CONNECTING:
            wlan.connect(wifi_ssid, wifi_password)
        time.sleep(2)
    print("\nConnected")

# This function sends data to an adafruit io feed using MQTT.
# It takes a number as input, and converts it to a string before sending it.
def mqtt_publish(data):
    global client, mqtt_topic
    print(f"Publish {data} ...", end='')
    if wlan.isconnected():
        print(" Done")
        client.publish(topic=mqtt_topic, msg=str(data))
    else:
        print(" Nope")

# This function updates the feed. It is required to have an input argument due to
# it being used as a timer callback:


# Connect to wifi:
connect_wlan()

# Create an MQTT client:
client = MQTTClient(
    mqtt_device_id,
    "io.adafruit.com",
    user=aio_username,
    password=aio_api_key,
    port=1883
)

# Connect the MQTT client:
client.connect()

# Loop
while True:
    data = randint(200, 300)
    mqtt_publish(data)
    time.sleep(10)
 
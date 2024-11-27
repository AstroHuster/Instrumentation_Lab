import time
import network
import rp2
from ReadTOML import settings

rp2.country("US")
print(f"settings['WIFI_SSID'] = {settings['WIFI_SSID']}")
print(f"settings['WIFI_PASSWORD'] = {settings['WIFI_PASSWORD']}")

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(settings['WIFI_SSID'], settings['WIFI_PASSWORD'])

while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting for Wi-Fi connection...")
    time.sleep(1)
print(wlan.ifconfig())
print(wlan.isconnected())

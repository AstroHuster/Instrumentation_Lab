import machine
import utime

#button = machine.Pin(15,machine.Pin.IN,machine.Pin.PULL_DOWN)

led_ext = machine.Pin(15,machine.Pin.OUT)

while True:
    if button.value()==1:
        led_ext.value(1)
        #utime.sleep(2)
    led_ext.value(0)
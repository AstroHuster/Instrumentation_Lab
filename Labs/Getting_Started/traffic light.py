import machine
import utime
import _thread

led_R = machine.Pin(15, machine.Pin.OUT)
led_Y = machine.Pin(14, machine.Pin.OUT)
led_G = machine.Pin(13, machine.Pin.OUT)

button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)
buzzer = machine.Pin(12, machine.Pin.OUT)

global button_pressed
button_pressed = False

def button_reader_thread():
    global button_pressed
    while True:
        if button.value() == 1:
            button_pressed = True
        utime.sleep(0.01)
_thread.start_new_thread(button_reader_thread,())


while True:
    if button_pressed == True:
        led_R.value(1)
        for i in range(10):
            buzzer.value(1)
            utime.sleep(0.2)
            buzzer.value(0)
            utime.sleep(0.2)
        global button_pressed
        button_pressed=False
    led_R.value(1)
    utime.sleep(5)
    led_Y.value(1)
    utime.sleep(2)
    led_R.value(0)
    led_Y.value(1)
    led_G.value(1)
    utime.sleep(5)
    led_G.value(0)
    led_Y.value(1)
    utime.sleep(5)
    led_Y.value(0)
    
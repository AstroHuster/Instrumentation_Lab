from machine import Pin
from time import sleep

COUNT_TIME = 60 # one minute
STOP_TIME = 5 * COUNT_TIME # five minutes

# Set up pin for interrupt counting when pulled low
counting_pin = Pin(16, Pin.IN, Pin.PULL_UP)

counts = 0
def count(int_pin):
    global counts
    counts += 1

counting_pin.irq(count, Pin.IRQ_FALLING, hard=True)


t_start = time()
t_stop = t_start + STOP_TIME
counts = 0
while time() < t_stop:
    sleep(1.0)
    print(counts)

print("# Time is up!")
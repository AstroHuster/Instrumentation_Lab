from machine import Pin
from time import time_ns

COUNT_TIME = 60 # one minute
STOP_TIME = 5 * 60 # five minutes

# Set up pin for interrupt counting when pulled low
counting_pin = Pin(16, Pin.IN, Pin.PULL_UP)

counts = 0
def count(int_pin):
    global counts
    counts += 1

counting_pin.irq(count, Pin.IRQ_FALLING, hard=True)

t_start_ns = time_ns()
t_stop_ns = t_start_ns + 1_000_000_000 * STOP_TIME
dt_count_ns = 1_000_000_000 * COUNT_TIME
t_next_ns = t_start_ns + dt_count_ns

while time_ns() < t_stop_ns:
    if time_ns() > t_next_ns:
        print((time_ns() - t_start_ns) // 1_000_000_000, counts)
        counts = 0
        t_next_ns += dt_count_ns
        
print((time_ns() - t_start_ns) // 1_000_000_000, counts)
print("# Time is up!")
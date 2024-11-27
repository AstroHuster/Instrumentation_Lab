""" counter_sim.py - simulates counting radiation

"""
from machine import Pin, Timer
from time import sleep, time_ns
from random import randint

COUNT_PER_SECOND = 1
PIN_COUNTING = 16
PIN_SIM = 17

# Counting parameters
COUNT_TIME = 10 # one minute
STOP_TIME = 100 * 10 # five minutes

# Simulation parameters
# Simulate 1 count per second
DT_SIM = 0.01 # interval time
DT_SIM_MS = round(1000 * DT_SIM)
N_PROB = round(1 / (COUNT_PER_SECOND * DT_SIM)) # prob per interval
print("# ", DT_SIM, DT_SIM_MS, N_PROB)



# Set up pin for interrupt counting when pulled low
counting_pin = Pin(PIN_COUNTING, Pin.IN, Pin.PULL_UP)

counts = 0
def count(int_pin):
    global counts
    counts += 1
counting_pin.irq(count, Pin.IRQ_FALLING, hard=True)

# Set up a Timer and start counting simulation
pin_sim = Pin(PIN_SIM, Pin.OUT, value=1)
led = Pin("LED", Pin.OUT)
count_me = 0
def sim_irq(pin_sim):
    global count_me
    led(0)
    if randint(1, N_PROB) == 1:
        count_me = 1
        led(1)
        # print("|", end='')
    # else:
        # print("_", end='')


timer_sim = Timer(period=DT_SIM_MS, mode=Timer.PERIODIC, callback=sim_irq)

        
# Start loop
t_start_ns = time_ns()
t_stop_ns = t_start_ns + 1_000_000_000 * STOP_TIME
dt_count_ns = 1_000_000_000 * COUNT_TIME
t_next_ns = t_start_ns + dt_count_ns
counts = 0
while time_ns() < t_stop_ns:
    if time_ns() > t_next_ns:
        print((time_ns() - t_start_ns) // 1_000_000_000, counts//2)
        counts = 0
        t_next_ns += dt_count_ns
    if count_me:
        counts += 1
        pin_sim(0)
        sleep(10e-6)
        pin_sim(1)
        count_me = 0
        # print('.', end='')
        
print((time_ns() - t_start_ns) // 1_000_000_000, counts)
# Turn off timer and counting
timer_sim.deinit()
counting_pin.irq(handler=None)

print("# Time is up!")
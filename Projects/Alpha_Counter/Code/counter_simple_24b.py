from machine import Pin
from time import time, sleep
from math import sqrt

print("# counter_simple_24")

COUNT_TIME = 60 # one minute
STOP_TIME = 15 * COUNT_TIME # five minutes
COUNT_PIN = 15

# Set up pin for interrupt counting when pulled low
counting_pin = Pin(COUNT_PIN, Pin.IN, Pin.PULL_UP)

counts = 0
def count(int_pin):
    global counts
    counts += 1

counting_pin.irq(count, Pin.IRQ_FALLING, hard=True)

# dd comments
done = False
while not done:
    line = input("# Add comment. Return to end: ").strip()
    if line:
        print('# ', line)
    else:
        done = True

t_start = time()
t_stop = t_start + STOP_TIME
counts = 0
counts_avg = 0.0
counts_std = 0.0
n_loops = 0
while time() < t_stop:
    sleep(1.0)
    print(f"{counts}, {int(counts_avg)}")
    n_loops += 1
    counts_avg += counts
    counts_std += counts * counts
    counts = 0

print("# Time is up!")

total_counts = counts_avg
counts_avg /= n_loops
counts_std = sqrt(counts_std / n_loops - counts_avg**2)
print(f"# Avg = {counts_avg}, std = {counts_std}, Sqrt(avg) = {sqrt(counts_avg)}")
print(f"# {total_counts} in {STOP_TIME} s")
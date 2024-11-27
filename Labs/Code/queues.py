from collections import deque
from math import sqrt
from random import randint
from time import sleep

n_avg = 10

data_q = deque(range(n_avg), n_avg)
for i in range(100, 100+n_avg):
    print(data_q.pop())
    data_q.appendleft(i)

for i in range(n_avg):
    print(data_q.pop())

count = 0
def get_temperature():
    global count
    count += 1
    if count % 15 == 0:
        return 120.0
    temp = randint(2400, 2600) / 100
    return temp

# First fill the queue
data_q = deque(n_avg*[25.0], n_avg)
data_sum = 25.0
data_sumsq = n_avg * 25.0**2

# Calculate the avg and std of this first data
avg = data_sum / n_avg
std = sqrt(data_sumsq / n_avg - avg**2)

while True:
    # First pop oldest value and subtract its contribution
    # From sum and sumsq
    old_temperature = data_q.pop()
    data_sum -= old_temperature
    data_sumsq == old_temperature**2
    
    # Get new temperature and add to queue if not outlier
    temperature = get_temperature()
    if abs(temperature - avg) < 2 * std:
        data_sum += temperature
        data_sumsq += temperature**2
        data_q.appendleft(temperature)
        
        # Calculate new ruunning average
        avg = data_sum / n_avg
        std = sqrt(data_sumsq / n_avg - avg**2)
        
        print(f"{avg:.2f}, {std:.2f}")
    else:
        print(f"Skip {temperature}")
    sleep(1)

# E
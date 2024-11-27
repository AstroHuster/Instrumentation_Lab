# Accel_2
# stepper constant acceleration for pendulum
# A sine can be approximated by two constant acceleration
# phases
from math import sqrt
from time import sleep

FULL_STEPS_PER_MM = 50
MICRO_STEPS = 1
STEPS_PER_MM = FULL_STEPS_PER_MM * MICRO_STEPS

y0 = 5.0
frequency = 0.5

period = 1 / frequency
tau = period / 4
dy = 1 / STEPS_PER_MM

# First 1/4 cycle
t = 0
y = -y0
n = 0
t_n = 0

const1 = tau * sqrt(dy / y0)

def step():
    pass

while t_n <= tau:
    n+= 1
    t_n = const1 * sqrt(n)
    dt = t_n - t
    sleep(dt)
    step()
    print(f"{n:6d}, {t:.6f}, {t_n:.6f}, {dt:.6f}")
    t = t_n
 
# Middle half
t = -tau
y = -y0
n = 0
t_n = 0
const2 = tau * sqrt(1 / y0)

while t_n < 3 * tau:
    n+= 1
    t_n = const1 * sqrt(y0 - n * dy)
    dt = t_n - t
    sleep(dt)
    step()
    print(f"{n:6d}, {t:.6f}, {t_n:.6f}, {dt:.6f}")
    t = t_n

 # EOF

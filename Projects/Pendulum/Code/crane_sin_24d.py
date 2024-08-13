""" crane_sine.py - Move the pendulum support in sinusoidal motion.

ProfHuster@GMail.com
2024-07-22

24b - change from stepping the derivative to calculating position
        and calculating steps from that.
24c - Added stepping to a position. If there return. With this I can
        call it at a high frequency and it won't matter. Probably so
        that it only takes one step at a time.
24d - Added x and MODE to Stepper class
"""
from math import pi, sin
from stepper_A4988 import Stepper
from time import ticks_us, ticks_diff

STEP_RATE = 2000 # Step rate for stepper motor driver
T_STOP = 1e6 * 10
AMP = 5.0 # mm
FREQ = 0.705

# Use  default pins. See module
crane = Stepper(rate=STEP_RATE)
crane.enable()
print(f"""x = {crane.x} mm,
mode = {crane.mode},
steps_per_mm = {crane.steps_per_mm}""")

# Move at a constant velocity
V0 = 20.0 # mm/s
DT = 0.00001 # Seconds per to_x
dt_us = round(1e6 * DT)
t0_us = ticks_us()
next_t = dt_us
try:
    while ticks_diff(ticks_us(), t0_us) < T_STOP:
        t = ticks_diff(ticks_us(), t0_us)
        if t > next_t:
            # Time to make a step
            x1 = AMP * sin(2 * pi * FREQ * 1e-6 * t)
            #print(x1)
            crane.to_x(x1)
            next_t += dt_us
        else:
            pass
except:
    print("Except!")
crane.to_x(0)
crane.disable()
print("D O N E ! ! !")

# End Of File
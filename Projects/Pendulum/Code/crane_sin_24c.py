""" crane_sine.py - Move the pendulum support in sinusoidal motion.

ProfHuster@GMail.com
2024-07-22

24b - change from stepping the derivative to calculating position
        and calculating steps from that.
24c - Added stepping to a position. If there return. With this I can
        call it at a high frequency and it won't matter. Probably so
        that it only takes one step at a time.
"""
from math import pi, cos
from stepper_A4988 import Stepper
from time import time, sleep_us, ticks_ms, ticks_diff

STEP_MODE = 4
STEPS_PER_MM = STEP_MODE * 1000.0 / 200.0 # Full step mode

AMP = 20.0 # mm
FREQ = 1.0 # Hz
STEP_RATE = 500 # Step rate for stepper motor driver
UPDATE_RATE = 5000
DT_US = round(1e6 / UPDATE_RATE) # update time for stepper position

N_CYCLES = 10
T0 = 1.0 / FREQ
T_END_MS = 1e3 * N_CYCLES * T0

two_pi_f_ms = 1e-3 * 2 * pi * FREQ

# Use  default pins. See module
crane = Stepper(rate=STEP_RATE)
crane.x = 0.0

def set_x(x):
    crane.x = x
def get_x():
    return crane.x
def to_x(x1=0.0):
    steps = round((x1 - crane.x) * STEPS_PER_MM)
    # print(steps)
    crane.x += steps / STEPS_PER_MM
    if steps:
        crane.do_steps(steps)
    return crane.x

crane.enable()
t0_ms = ticks_ms()
set_x(0)
while ticks_diff(ticks_ms(), t0_ms) < T_END_MS:
    pos_next = round(AMP * cos(two_pi_f_ms * ticks_diff(ticks_ms(),t0_ms)))
    to_x(pos_next)
    sleep_us(DT_US)

t1_ms = ticks_ms()
t_cycles = 1e-3 * ticks_diff(t1_ms, t0_ms)
crane.disable()

print(f"{N_CYCLES} took {t_cycles} s, so freq = {N_CYCLES / t_cycles}")

print("D O N E ! ! !")

# End Of File
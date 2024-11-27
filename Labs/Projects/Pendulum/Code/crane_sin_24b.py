""" crane_sine.py - Move the pendulum support in sinusoidal motion.

ProfHuster@GMail.com
2024-07-22

24b - change from stepping the derivative to calculating position
        and calculating steps from that.
"""
from math import pi, sin
from stepper_A4988 import Stepper
from time import sleep_us, time

STEPS_PER_MM = 1000.0 / 200.0

AMP = 20.0 # mm
FREQ = 0.8 # Hz
DT = 0.005 # s update time for stepper
STEP_RATE = 500

N_CYCLES = 3

amp_steps = AMP * STEPS_PER_MM
two_pi_f = 2 * pi * FREQ
sleep_dt_us = round(1e6 * DT)
dt_per_step_us = 1e6 / STEP_RATE

T0 = 1.0 / FREQ
print(amp_steps, two_pi_f, sleep_dt_us)
dt_per_cycle = T0 / DT
print(f"There are {dt_per_cycle} time steps per cycle.")

# Use  default pins. See module
crane = Stepper(rate=STEP_RATE)

n_dt = round(N_CYCLES * dt_per_cycle)

t_i = 0
crane.enable()
t0 = time()
pos0 = 0
for i in range(n_dt):
    t_i += DT
    pos_next = round(amp_steps * sin(two_pi_f * t_i))
    d_pos = pos_next - pos0
    crane.do_steps(d_pos)
    sleep_us(round(sleep_dt_us - abs(d_pos) * dt_per_step_us))
    pos0 = pos_next

t1 = time()
crane.disable()

print(f"{N_CYCLES} took {t1 - t1} s, so freq = {N_CYCLES / (t1 - t0)}")

print("D O N E ! ! !")

# End Of File
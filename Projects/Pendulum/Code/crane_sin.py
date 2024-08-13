""" crane_sine.py - Move the pendulum support in sinusoidal motion.

ProfHuster@GMail.com
2024-07-22

"""
from math import pi, cos
from stepper_A4988 import Stepper
from time import sleep_us, time

STEPS_PER_MM = 1000.0 / 200.0

AMP = 1.0 # mm
FREQ = 1.0 # Hz
DT = 0.01 # s update time for stepper
STEP_RATE = 500

N_CYCLES = 3

amp_steps = AMP * STEPS_PER_MM
two_pi_f = 2 * pi * FREQ
two_pi_f_a = amp_steps * two_pi_f
sleep_dt_us = round(1e6 * DT)

T0 = 1.0 / FREQ
print(amp_steps, two_pi_f, two_pi_f_a, sleep_dt_us)
dt_per_cycle = T0 / DT
print(f"There are {dt_per_cycle} time steps per cycle.")

# Use  default pins. See module
crane = Stepper(rate=STEP_RATE)

n_dt = round(N_CYCLES * dt_per_cycle)

t_i = 0
crane.enable()
t0 = time()
for i in range(n_dt):
    t_i += DT
    steps_i = round(two_pi_f_a * cos(two_pi_f * t_i))
    # print(t_i, steps_i)
    crane.do_steps(steps_i)
    sleep_us(sleep_dt_us)

t1 = time()
crane.disable()

print(f"{N_CYCLES} took {t1 - t1} s, so freq = {(t1 - t0) / N_CYCLES}")

print("D O N E ! ! !")

# End Of File
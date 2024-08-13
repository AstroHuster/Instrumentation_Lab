from stepper import Stepper
import time

s1 = Stepper(18,19,steps_per_rev=200,speed_sps=50)
s2 = Stepper(20,21,steps_per_rev=200,speed_sps=50)

s1.target_deg(90)
s2.target_deg(45)
time.sleep(5.0)
s1.target_deg(0)
s2.target_deg(5)
time.sleep(5.0)
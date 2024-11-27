from time import sleep
from FunctionGenerator import waveform
# FunctionGenerator.py needs to be on the Pico

# make a waveform with default attributes
wave1=waveform()

# turn it on
wave1.run(1)
# wait
sleep(3)
# turn it off
wave1.run(0)
# celebrate
print("ta da")


# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple demo of writing a sine wave to the AD569x DAC.
Uses a timer and interrupt.
"""

import time
from math import sin, pi
from array import array
from time import sleep
from machine import Pin, I2C, ADC, PWM
from ad593x import AD593x

FREQ_SIG = int(input("Enter signal frequency: "))
N_LUT = 1<<5 # 32
LUT_MASK = N_LUT - 1
FREQ_SAMP = N_LUT * FREQ_SIG
DT = 1 / FREQ_SAMP
print('DT,       SAMP, SIG, LUT MASK')
print(1e6*DT, FREQ_SAMP, FREQ_SIG, hex(LUT_MASK), '\n')

# Set up adc to read DAC output
adc = ADC(Pin(26))

# Setup up DAC
sda = Pin(16, Pin.OUT)
scl = Pin(17, Pin.OUT)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=400_000)
dac = AD593x(i2c)
dac.reset()
dac.config(gain=0, ref=1)

# Set up timer and ISR to write to the DAC
lut = array('i', [0xffff & int(0x7ffe * sin(2 * pi * i / N_LUT) + 0x7fff) for i in range(N_LUT)])
for i in range(N_LUT):
    print(f"{hex(lut[i]):6s}", end='\n' if i % 4 == 3 else ',')

# The Timer ISR
_I_DAC = 0
def adc_write(t):
    global _I_DAC, LUT_MASK
    _I_DAC &= LUT_MASK
    dac.write(lut[_I_DAC])
    _I_DAC += 1

# Set up PWM to Pin 0, then Pin 1 ISR
# Wire pin0 to pin1
p0 = Pin(0, Pin.OUT)
p1 = Pin(1, Pin.IN)

# Start Pin 0 PWM. Defaults to 50% duty cycle
pwm0 = PWM(Pin(0), freq=FREQ_SAMP, duty_u16=0x7fff)

# Set up Pin 1 ISR to write DAC
p1.irq(trigger=machine.Pin.IRQ_RISING, handler=adc_write)

while True:
    sleep(DT)
    # print(f"{adc.read_u16():5d}")


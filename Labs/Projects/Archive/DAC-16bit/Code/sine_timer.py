# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple demo of writing a sine wave to the AD569x DAC.
Uses a timer and interrupt.
"""

import time
from math import sin, pi
from time import sleep
from machine import Pin, I2C, ADC
from machine import Timer
from ad593x import AD593x

DEBUG = False
DT_MS = 1 # Set in ms
DT = 1e-3 * DT_MS
FREQ_SAMP = 1 / DT
FREQ_SIG = 50.0
print(DEBUG, DT_MS, DT, FREQ_SAMP, FREQ_SIG)

# Set up adc to read DAC output
adc = ADC(Pin(26))
sda = Pin(16, Pin.IN)
scl = Pin(17, Pin.IN)

# Setup up DAC
i2c=machine.I2C(0,sda=sda, scl=scl, freq=400_000)
dac = AD593x(i2c)
dac.reset()
dac.config()

# Set up timer and ISR to write to the DAC
_I_DAC = 0
_DAC_VALUE = 0
_SIN_ARG = 2 * pi * FREQ_SIG * DT

# The Timer ISR
def adc_write(t):
    global _I_DAC, _DAC_VALUE
    _DAC_VALUE = 0xFFFF & \
            int(0x7FFE * sin(_SIN_ARG * _I_DAC) + 0x7FFF)
    dac.write(_DAC_VALUE)
    _I_DAC += 1

timer = Timer(-1)
timer.init(mode=Timer.PERIODIC, period=DT_MS, callback=adc_write)

while True:
    sleep(DT)
    if DEBUG:
        print(f"{adc.read_u16():5d}")


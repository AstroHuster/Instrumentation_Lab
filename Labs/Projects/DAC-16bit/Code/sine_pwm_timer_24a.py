# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple demo of writing a sine wave to the AD569x DAC.
Uses a timer and interrupt.
"""

import time
from math import sin, pi
from time import sleep
from machine import Pin, I2C, ADC, PWM
from ad593x import AD593x

DEBUG = False
FREQ_SAMP = 2_000
DT = 1 / FREQ_SAMP
FREQ_SIG = 50.0
print(DEBUG, DT, FREQ_SAMP, FREQ_SIG)

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
    _I_DAC += 1
    dac.write(_DAC_VALUE)

# Set up PWM to Pin 0, then Pin 1 ISR
# Wire pin0 to pin1
p0 = Pin(0, Pin.OUT)
p1 = Pin(1, Pin.IN)

# Start Pin 0 PWM. Defaults to 50% duty cycle
pwm0 = PWM(Pin(0), freq=FREQ_SAMP, duty_u16=0x7fff)

# Set up Pin 1 ISR to write DAC
p1.irq(trigger=machine.Pin.IRQ_RISING, handler=adc_write)

if DEBUG:
    while True:
        sleep(DT)
        print(f"{adc.read_u16():5d}")


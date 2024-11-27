# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple demo of writing a sine wave to the AD569x DAC."""

import time
from math import sin, pi
from time import sleep
from machine import Pin, I2C, ADC
from ad593x import AD593x

FREQ_SIG = 1.0
FREQ_SAMP = 32 * FREQ_SIG
DT = 1 / FREQ_SAMP

# Set up adc to read DAC output
adc = ADC(Pin(26))
sda = Pin(16, Pin.IN)
scl = Pin(17, Pin.IN)

# Setup up DAC
i2c=machine.I2C(0,sda=sda, scl=scl, freq=100_000)
dac = AD593x(i2c)
dac.reset()
dac.config()

i_t = 0
while True:
    value = 0xFF & \
            int(0x7FFE * sin(2 * pi * FREQ_SIG * i_t * DT) + 0x7FFF)
    dac.write(value)
    sleep(DT)
    i_t += 1
    print(f"{adc.read_u16():5d}")


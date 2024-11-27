# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple demo of writing a sine wave to the AD569x DAC."""

import time
import math
from machine import Pin, I2C
from my_ad569x import Adafruit_AD569x

DAC_addr = 0x4c

# i2c = busio.I2C(board.SCL, board.SDA, frequency=400_000)
sda = Pin(16, Pin.IN)
scl = Pin(17, Pin.IN)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=400_000)

# Initialize AD569x
dac = Adafruit_AD569x(i2c, DAC_addr)

# ADC
adc = analogio.AnalogIn(board.GP26_A0)

# sine wave values written to the DAC
value = [
    int(math.sin(math.pi * 2 * i / LENGTH) * ((2**15) - 1) + 2**15)
    for i in range(LENGTH)
]

while True:
    for v in value:
        dac.value = v
        time.sleep(T_SLEEP)
        print(f"{adc.value:5d}")


# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple demo of writing a sine wave to the AD569x DAC."""

import time
import math
import board
import busio
import analogio
import adafruit_ad569x

# length of the sine wave
LENGTH = 100

T_SLEEP = 5 / LENGTH

# i2c = busio.I2C(board.SCL, board.SDA, frequency=400_000)
i2c = busio.I2C(board.GP17, board.GP16, frequency=400_000)

# Initialize AD569x
dac = adafruit_ad569x.Adafruit_AD569x(i2c)

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

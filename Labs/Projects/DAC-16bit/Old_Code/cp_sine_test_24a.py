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
FR_SIG = 24.0
FR_SAMP = 100 * FR_SIG
DT = 1 / FR_SAMP

# i2c = busio.I2C(board.SCL, board.SDA, frequency=400_000)
i2c = busio.I2C(board.GP17, board.GP16, frequency=400_000)

# Initialize AD569x
dac = adafruit_ad569x.Adafruit_AD569x(i2c)

# ADC
adc = analogio.AnalogIn(board.GP26_A0)

i = 0
while True:
    value0 = int(0x7ffe * math.sin(2 * math.pi * FR_SIG * i * DT) + 0x7fff)
    dac.value = value0
    time.sleep(DT)
    i += 1
    # print(f"{adc.value:5d}")
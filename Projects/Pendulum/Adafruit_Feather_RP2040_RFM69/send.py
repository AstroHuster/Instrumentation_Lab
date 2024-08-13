# SPDX-FileCopyrightText: 2023 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
CircuitPython Feather RP2040 RFM69 Packet Send Demo

This demo sends a "button" packet when the Boot button is pressed.

This example is meant to be paired with the Packet Receive Demo code running
on a second Feather RP2040 RFM69 board.
"""

import board
import digitalio
import keypad
import adafruit_rfm69
from random import uniform
from time import sleep, monotonic

print("Feather RP20240 RFM69 Send Demo")

T_SEND = 0.1
N_LOOP = 100

# 1/s 6.70 ms
# 10/2 5.811 ms
# 100/s 5.92 ms

# Set up button using keypad module.
button = keypad.Keys((board.BUTTON,), value_when_pressed=False)

# Define radio frequency in MHz. Must match your
# module. Can be a value like 915.0, 433.0, etc.
RADIO_FREQ_MHZ = 915.0

# Define Chip Select and Reset pins for the radio module.
CS = digitalio.DigitalInOut(board.RFM_CS)
RESET = digitalio.DigitalInOut(board.RFM_RST)

# Initialise RFM69 radio
rfm69 = adafruit_rfm69.RFM69(board.SPI(), CS, RESET, RADIO_FREQ_MHZ)

for _ in range(10):
    t0 = monotonic()
    for i_loop in range(N_LOOP):
        sleep(T_SEND)
        buf_out = bytes(str(uniform(0, 10)), "UTF-8")
        rfm69.send(buf_out)
        # print(end='.')
    print()

    t_loop = (monotonic() - t0) / N_LOOP
    print(f"t_loop = {t_loop} set is {T_SEND}")

""" run_dac.py """
_I2CADDR = 0x4C

import time
from machine import Pin, ADC
from micropython import const
import math

_WRITE_CONTROL = const(0x40)
_WRITE_DAC_AND_INPUT = const(0x30)

DAC_addr = 0x4c
ADC_pin = 'GP26'

# i2c = busio.I2C(board.SCL, board.SDA, frequency=400_000)
# sda = Pin(16, Pin.IN)
sda = Pin('GP16', Pin.IN)
scl = Pin('GP17', Pin.IN)
print("i2c = ")
i2c = machine.I2C(0,sda=sda, scl=scl, freq=400_000)

# Set up ADC
adc = ADC(26)

print(f"{hex(i2c.scan()[0])}")

addr = DAC_addr

def _send_command(command: int, data: int) -> None:
    """
    Send a command and data to the I2C device.

    This internal function prepares a 3-byte buffer containing the command and data,
    and writes it to the I2C device.

    :param command: The command byte to send.
    :param data: The 16-bit data to send.
    """
    try:
        high_byte = (data >> 8) & 0xFF
        low_byte = data & 0xFF
        buffer = bytearray([command, high_byte, low_byte])
    except Exception as error:
        raise error

_mode = 0 # Normal vs imedance or tristate
_internal_reference = 1 # External reference
_gain = 0 # 0 to Vref

def _update_control_register():
    data = 0x0000
    data |= _mode << 13
    data |= not _internal_reference << 12
    data |= _gain << 11
    _send_command(_WRITE_CONTROL, data)

def reset():
    reset_command = 0x8000
    try:
        _send_command(_WRITE_CONTROL, reset_command)
    except OSError as error:
        raise Exception(f"Error during reset: {error}") from error

def value(val: int) -> None:
    _send_command(_WRITE_DAC_AND_INPUT, val)

print("reset")
reset()
print("_update_control_register")
_update_control_register()

for i in range(100):
    value(0)
    time.sleep(0.2)
    value(0x7fff)
    time.sleep(0.2)

while True:
    for i in range(0, 0xffff, 0xff):
        value(i)
        time.sleep(0.1)
        print(adc.read_u16())
    
print("D O N E")

def dac_sin(i, dt):
    val = int(math.sin(2 * math.pi * freq * i * dt) * 0x7ffe + 0x7fff)
    return val
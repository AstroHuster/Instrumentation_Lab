""" test_DAC.py
"""
print("test_DAC.py")

from machine import Pin, ADC
from time import sleep

N_LOOPS = 10

# Set the output pins to the DAC
p7 = Pin(7, Pin.OUT)
p6 = Pin(6, Pin.OUT)
p5 = Pin(5, Pin.OUT)
p4 = Pin(4, Pin.OUT)
p3 = Pin(3, Pin.OUT)
p2 = Pin(2, Pin.OUT)
p1 = Pin(1, Pin.OUT)
p0 = Pin(0, Pin.OUT)
pins = [p0, p1, p2, p3, p4, p5, p6, p7]

# Set up the ADC to read the DAC output signal
adc_sig = ADC(Pin(26, Pin.IN))
adc_gndv = ADC(Pin(27, Pin.IN))

# Code to set DAC
def set_dac(x):
    # Make sure s is in range
    # The & is the "bitwise and" operator
    x &= 0xff
    # Set each pin
    for i_bit in range(8):
        # Fancy way of testing if bit is high
        if x & (1<<i_bit):
            pins[i_bit].high()
        else:
            pins[i_bit].low()
            
# Turn off the DAC
set_dac(0)
sleep(1)

# Function to read the signal out voltage
# and the virtual gound voltage
def adc_v():
    val_sig = adc_sig.read_u16()
    Vsig = 3.3 * val_sig / 0xffff
    val_gndv = adc_gndv.read_u16()
    Vgndv = 3.3 * val_gndv / 0xffff
    return Vsig, Vgndv

# Select 4 or 8 bit mode
answer = input("Test as a 4-bit or 8-bit DAC (Enter 4 or 8): ")
n_bits = int(answer)
# Make the default 8-bits
if n_bits != 4:
    n_bits = 8
print(f"Testing {n_bits} bit mode")

n_steps = 1 << n_bits
# Repeat the measurements N_LOOP times
for i_loop in range(N_LOOPS):
    # Loop over every DAC step
    for i in range(n_steps):
        # For 8-bits use evey number
        if n_bits == 8:
            set_dac(i)
            sleep(0.1)
        else:
            # For 4-bit count by 16
            set_dac(16 * i)
            sleep(16 * 0.1)
        # Take data and print it
        (Vsig, Vgndv) = adc_v()
        print(f"{i:4d} {Vsig:7.4f} {Vgndv:7.4f} {Vsig - Vgndv:7.4f}")

set_dac(0)
print("D-O-N-E-!")
# EOF
"""Simple test of PWM trigggering an ISR

CONCLUSIONS:
- Calculating the sin for output take 313 us/loop
- Calculating a parabola approx taks 126 us/loop
- Using a Look Up Table (LUT) takes 17.1 us/loop

PWM Speed
With the default CPU speed of 125 MHz the fastest speed was 20 kHz
Overclocking to 250 MHz, the fastest speed was 40 kHz
"""
import time
from math import sin, cos, pi
from machine import Pin, I2C, ADC, PWM
from machine import freq as cpu_freq
from ad593x import AD593x

CPU_FREQ  = 250_000_000
FREQ_SAMP = 6400 # Range frz, to 62.5 MHz
FREQ_I2S  = 400_000
n_lut = 0x20
FREQ_SIG  = FREQ_SAMP / n_lut
DT = 1 / FREQ_SAMP
DT_US = round(1_000_000 / FREQ_SAMP)

print(f"FREQ_I2S = {FREQ_I2S}")
print(f"FREQ_SIG  = {FREQ_SIG}")

cpu_freq(CPU_FREQ)
print(f"CPU_FREQ = {CPU_FREQ}\nActual   = {cpu_freq()}")

# Choose with or without DAC
use_dac = bool(input("Enter 1 to use the DAC, 0 for not: "))

# Set up adc to read DAC output
adc = ADC(Pin(26))

# Set up DAC
sda = Pin(16, Pin.IN)
scl = Pin(17, Pin.IN)
i2c = I2C(0,sda=sda, scl=scl, freq=FREQ_I2S)
dac = AD593x(i2c)
dac.reset()
dac.config()

# Time sin calculation
value = 0.0
SIN_ARG = 2 * pi * FREQ_SIG * DT
t0 = time.time_ns()
n_loops = 1_000
for i in range(n_loops):
    value = int(0x7FFE * sin(SIN_ARG * i)) + 0x7FFF
t1 = time.time_ns()
print(f"sin took {(t1 - t0) / (1_000 * n_loops)} us/loop")

# Now time cosine approximation
def cos_appx(x):
    x %= 2 * pi
    a = pi**2 / 4
    if x < 0.5 * pi:
        return -(x**2 - a)/a
    if x < 1.5 * pi:
        return ((x - pi)**2 - a)/a
    return -((x - 2 * pi)**2 - a)/a    

n_loops = 1_000
t0 = time.time_ns()
for i in range(n_loops):
    value = int(0x7FFE * cos_appx(SIN_ARG * i)) + 0x7FFF
t1 = time.time_ns()
print(f"cos_appx took {(t1 - t0) / (1_000 * n_loops)} us/loop")

# Now time cosine approximation
p2 = 2 * pi
ph = 0.5 * pi
p3h = 1.5 * pi
def cos_appx2(x):
    x %= p2
    a = pi*pi / 4
    if x < ph:
        return -(x*x - a)/a
    if x < p3h:
        xt = x - pi
        return (xt*xt - a)/a
    xt = x - p2
    return -(xt*xt - a)/a    

n_loops = 1_000
t0 = time.time_ns()
for i in range(n_loops):
    value = int(0x7FFE * cos_appx2(SIN_ARG * i)) + 0x7FFF
t1 = time.time_ns()
print(f"cos_appx2 took {(t1 - t0) / (1_000 * n_loops)} us/loop")

# Test lookup
from array import array
mask = 0x1f
lut = array('i', [int(0x7ffe * sin(2 * pi * i / n_lut) + 0x7fff) for i in range(n_lut)])

n_loops = 1_000
t0 = time.time_ns()
for i in range(n_loops):
    value = lut[i & mask]
t1 = time.time_ns()
print(f"lut took {(t1 - t0) / (1_000 * n_loops)} us/loop")

if not use_dac:
    # The Timer ISR setup
    pin2 = Pin(2, Pin.OUT, value=0)
    i_isr = 0
    def pwm_isr(t):
        global pin2, i_isr
        i_isr ^= 1 # toggle between 0 and 1
        pin2(i_isr)
        i_isr += 1

    # Set up PWM to Pin 0, then Pin 1 ISR
    # Wire pin0 to pin1
    # Start Pin 0 PWM. Defaults to 50% duty cycle
    p0 = Pin(0, Pin.OUT)
    pwm0 = PWM(p0, freq=FREQ_SAMP, duty_u16=0x7fff)
    print(f"FREQ_SAMP = {FREQ_SAMP}\nActual   = {pwm0.freq()}")
else:
    # The Timer ISR setup
    pin2 = Pin(2, Pin.OUT, value=0)
    i_isr = 0
    def pwm_isr(t):
        global i_isr, lut, mask
        dac.write(lut[i_isr & mask])
        i_isr += 1

    # Set up PWM to Pin 0, then Pin 1 ISR
    # Wire pin0 to pin1
    # Start Pin 0 PWM. Defaults to 50% duty cycle
    p0 = Pin(0, Pin.OUT)
    pwm0 = PWM(p0, freq=FREQ_SAMP, duty_u16=0x7fff)
    print(f"FREQ_SAMP = {FREQ_SAMP}\nActual   = {pwm0.freq()}")


# Set up Pin 1 ISR to write DAC
p1 = Pin(1, Pin.IN)
p1.irq(trigger=machine.Pin.IRQ_RISING, handler=pwm_isr)

# EOF
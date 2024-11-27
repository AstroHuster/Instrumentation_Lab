"""
AEG_Sines.py - generate a sweep of sinusoidal frequencies.

v24b - Enter fr0, fr1, df, offset, amplitude
v24c - Calculate Vavg, Vrms for each frequency
        Clean up after running with try/except and machine.reset()
        Clean up user interface
v24d - For filter measurment.
        adc_gndv (GP26/31) - GNDV
        adc_vsig (GP27/32) - VSIG
        adc_vfilt (GP28/34) - Filter output
"""
# Arbitrary waveform generator for Rasberry Pi Pico
# Requires 8-bit R2R DAC on pins 0-7. Works for R=1kOhm
# Achieves 125Msps when running 125MHz clock
# Rolf Oldeman, 13/2/2021. CC BY-NC-SA 4.0 licence
# tested with rp2-pico-20210205-unstable-v1.14-8-g1f800cac3.uf2
from machine import Pin, mem32, reset
from rp2 import PIO, StateMachine, asm_pio
from array import array
from time import sleep, sleep_us
from math import pi,sin,exp,sqrt,floor, log
from uctypes import addressof
from random import random

print("AWG_Sines.py")

print("NOTE: frequencies get rounded to the nearest integer")
ans = input("Enter log for logarithmic freq spacing (default lin): ")
if 'log' in ans:
    print("Logarithmic frequency sweep") 
    in_str = input("Enter f0, f1, nf (separated by spaces): ").split()
    fr0 = int(in_str[0])
    fr1 = int(in_str[1])
    nf = int(in_str[2])
    
    ln0 = log(fr0)
    ln1 = log(fr1)
    d_ln = (ln1 - ln0) / (nf -1)
    
    freqs = nf * [0]
    for i in range(nf):
        freqs[i] = round(exp(ln0 + i * d_ln))
else:
    print("Linear frequency sweep") 
    in_str = input("Enter f0, f1, df (separated by spaces): ").split()
    fr0 = int(in_str[0])
    fr1 = int(in_str[1])
    df = int(in_str[2])

    freqs = list(range(fr0, fr1 + df, df))
    
print(f"freqs = {freqs}")

try:
    offset = float(input("Enter offset (0 to 1): "))
    offset = max(min(1.0, offset), 0.0)
except ValueError:
    offset = 0.5

max_amp = min(offset, 1 - offset)

try:
    amplitude = float(input("Enter amplitude (0 to 0.5): "))
    amplitude = max(min(max_amp, amplitude), 0.0)
except ValueError:
    amplitude = 0.5
    
print(f"offset {offset:.3f}, amplitude {amplitude:.3f}")

# Set up adc
N_REPEAT = 100
N_PER_CYCLE = 32
N_CYCLES = 10
N_AVG = N_PER_CYCLE * N_CYCLES # 32 points per cycle x 10 cycles

from machine import ADC
adc_gndv = ADC(Pin(26, Pin.IN)) # GNDV
adc_vsig = ADC(Pin(27, Pin.IN)) # VSIG
adc_vfilt = ADC(Pin(28, Pin.IN)) # VFILT

adc_to_V = 3.3 / 0xffff

def read_v():
    # First read adc's
    gndv = adc_gndv.read_u16()
    vsig = adc_vsig.read_u16()
    vfilt = adc_vfilt.read_u16()
    # convert to voltage
    gndv *= adc_to_V
    vsig *= adc_to_V
    vfilt *= adc_to_V
    return (gndv, vsig, vfilt)

fclock=125000000 #clock frequency of the pico

DMA_BASE=0x50000000
CH0_READ_ADDR  =DMA_BASE+0x000
CH0_WRITE_ADDR =DMA_BASE+0x004
CH0_TRANS_COUNT=DMA_BASE+0x008
CH0_CTRL_TRIG  =DMA_BASE+0x00c
CH0_AL1_CTRL   =DMA_BASE+0x010
CH1_READ_ADDR  =DMA_BASE+0x040
CH1_WRITE_ADDR =DMA_BASE+0x044
CH1_TRANS_COUNT=DMA_BASE+0x048
CH1_CTRL_TRIG  =DMA_BASE+0x04c
CH1_AL1_CTRL   =DMA_BASE+0x050

PIO0_BASE      =0x50200000
PIO0_TXF0      =PIO0_BASE+0x10
PIO0_SM0_CLKDIV=PIO0_BASE+0xc8

#state machine that just pushes bytes to the pins
@asm_pio(out_init=(PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH,PIO.OUT_HIGH),
         out_shiftdir=PIO.SHIFT_RIGHT, autopull=True, pull_thresh=32)
def stream():
    out(pins,8)

sm = StateMachine(0, stream, freq=125000000, out_base=Pin(0))
sm.active(1)

#2-channel chained DMA. channel 0 does the transfer, channel 1 reconfigures
p=array('I',[0]) #global 1-element array
def startDMA(ar,nword):
    
    #first disable the DMAs to prevent corruption while writing
    mem32[CH0_AL1_CTRL]=0
    mem32[CH1_AL1_CTRL]=0
    #setup first DMA which does the actual transfer
    mem32[CH0_READ_ADDR]=addressof(ar)
    mem32[CH0_WRITE_ADDR]=PIO0_TXF0
    mem32[CH0_TRANS_COUNT]=nword
    IRQ_QUIET=0x1 #do not generate an interrupt
    TREQ_SEL=0x00 #wait for PIO0_TX0
    CHAIN_TO=1    #start channel 1 when done
    RING_SEL=0
    RING_SIZE=0   #no wrapping
    INCR_WRITE=0  #for write to array
    INCR_READ=1   #for read from array
    DATA_SIZE=2   #32-bit word transfer
    HIGH_PRIORITY=1
    EN=1
    CTRL0=(IRQ_QUIET<<21)|(TREQ_SEL<<15)|(CHAIN_TO<<11)|(RING_SEL<<10)|(RING_SIZE<<9)|(INCR_WRITE<<5)|(INCR_READ<<4)|(DATA_SIZE<<2)|(HIGH_PRIORITY<<1)|(EN<<0)
    mem32[CH0_AL1_CTRL]=CTRL0
    #setup second DMA which reconfigures the first channel
    p[0]=addressof(ar)
    mem32[CH1_READ_ADDR]=addressof(p)
    mem32[CH1_WRITE_ADDR]=CH0_READ_ADDR
    mem32[CH1_TRANS_COUNT]=1
    IRQ_QUIET=0x1 #do not generate an interrupt
    TREQ_SEL=0x3f #no pacing
    CHAIN_TO=0    #start channel 0 when done
    RING_SEL=0
    RING_SIZE=0   #no wrapping
    INCR_WRITE=0  #single write
    INCR_READ=0   #single read
    DATA_SIZE=2   #32-bit word transfer
    HIGH_PRIORITY=1
    EN=1
    CTRL1=(IRQ_QUIET<<21)|(TREQ_SEL<<15)|(CHAIN_TO<<11)|(RING_SEL<<10)|(RING_SIZE<<9)|(INCR_WRITE<<5)|(INCR_READ<<4)|(DATA_SIZE<<2)|(HIGH_PRIORITY<<1)|(EN<<0)
    mem32[CH1_CTRL_TRIG]=CTRL1



def setupwave(buf,f,w):
    div=fclock/(f*maxnsamp) # required clock division for maximum buffer size
    if div<1.0:  #can't speed up clock, duplicate wave instead
        dup=int(1.0/div)
        nsamp=int((maxnsamp*div*dup+0.5)/4)*4 #force multiple of 4
        clkdiv=1
    else:        #stick with integer clock division only
        clkdiv=int(div)+1
        nsamp=int((maxnsamp*div/clkdiv+0.5)/4)*4 #force multiple of 4
        dup=1

    #fill the buffer
    for isamp in range(nsamp):
        buf[isamp]=max(0,min(255,int(256*eval(w,dup*(isamp+0.5)/nsamp))))

    #set the clock divider
    clkdiv_int=min(clkdiv,65535) 
    clkdiv_frac=0 #fractional clock division results in jitter
    mem32[PIO0_SM0_CLKDIV]=(clkdiv_int<<16)|(clkdiv_frac<<8)

    #start DMA
    startDMA(buf,int(nsamp/4))


#evaluate the content of a wave
def eval(w,x):
    m,s,p=1.0,0.0,0.0
    if 'phasemod' in w.__dict__:
        p=eval(w.phasemod,x)
    if 'mult' in w.__dict__:
        m=eval(w.mult,x)
    if 'sum' in w.__dict__:
        s=eval(w.sum,x)
    x=x*w.replicate-w.phase-p
    x=x-floor(x)  #reduce x to 0.0-1.0 range
    v=w.func(x,w.pars)
    v=v*w.amplitude*m
    v=v+w.offset+s
    return v

#some common waveforms. combine with sum,mult,phasemod
def sine(x,pars):
    return sin(x*2*pi)
def pulse(x,pars): #risetime,uptime,falltime
    if x<pars[0]: return x/pars[0]
    if x<pars[0]+pars[1]: return 1.0
    if x<pars[0]+pars[1]+pars[2]: return 1.0-(x-pars[0]-pars[1])/pars[2]
    return 0.0
def gaussian(x,pars):
    return exp(-((x-0.5)/pars[0])**2)
def sinc(x,pars):
    if x==0.5: return 1.0
    else: return sin((x-0.5)/pars[0])/((x-0.5)/pars[0])
def exponential(x,pars):
    return exp(-x/pars[0])
def noise(x,pars): #p0=quality: 1=uniform >10=gaussian
    return sum([random()-0.5 for _ in range(pars[0])])*sqrt(12/pars[0])
    

#make buffers for the waveform.
#large buffers give better results but are slower to fill
maxnsamp=4096 #must be a multiple of 4. miximum size is 65536
wavbuf={}
wavbuf[0]=bytearray(maxnsamp)
wavbuf[1]=bytearray(maxnsamp)
ibuf=0

#empty class just to attach properties to
class wave:
    pass


wave1=wave()
wave1.amplitude = amplitude
wave1.offset = offset
wave1.phase=0.0
wave1.replicate=1
wave1.func=sine
wave1.pars=[]

print("#step through frequencies")
try:
    for i in range(N_REPEAT):
        print(f"# Loop {i:5d}/{N_REPEAT:5d}")
        for freq in freqs:
            t_sleep_us = round(1_000_000 / (N_PER_CYCLE * freq))
            print(t_sleep_us, end=' ')
            setupwave(wavbuf[ibuf],freq,wave1); ibuf=(ibuf+1)%2
            sleep(1)
            sum_Vsig = 0.0
            sum_Vsig2 = 0.0
            sum_Vfilt = 0.0
            sum_Vfilt2 = 0.0
            for i in range(N_AVG):
                # Read voltages relative to virtual ground
                (vg, vs, vf) = read_v()
                vs -= vg
                vf -= vg

                # Cum sums for sig, filt and std's
                sum_Vsig += vs
                sum_Vsig2 += vs * vs
                sum_Vfilt += vf
                sum_Vfilt2 += vf * vf
                
                # Pause
                sleep_us(t_sleep_us)
                
            V_sig = sum_Vsig / N_AVG
            V_sig_rms = sqrt(sum_Vsig2 / N_AVG - V_sig * V_sig)
            V_filt = sum_Vfilt / N_AVG
            V_filt_rms = sqrt(sum_Vfilt2 / N_AVG - V_filt * V_filt)
            print(\
f"{freq:6d} {V_sig:7.4f} {V_sig_rms:7.4f} {V_filt:7.4f} {V_filt_rms:7.4f}")
            # End loop
finally:
    print("Clean up")
    # Turn off statemachine
    # sm.active(0) # Nope
    # PIO.remove_program(stream) # Nope
    reset()
    

print("D O N E ! ! !")
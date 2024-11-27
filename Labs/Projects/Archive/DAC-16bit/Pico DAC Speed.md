# Pico DAC Speed

The RP2040 timers in uPy have a maximum frequency of 1 kHz, so that won't work for 
generating a since wave. I posted on a forum and someone suggested use a PWM to 
trigger an interrupt on a second pin. That works.

**Setup** 
- Use GP0 as the PWM pin.
- Wire GP0 to GP1.
- Set up an ISR on GP1.

This works. I did that and tried to synthesize a sine wave. I tested how fast I could 
push the PWM method by have a stripped down ISR that toggles pin GP1 on every 
call. 

**Results**
- With the default CPU speed of 125 MHz the fastest speed was 20 kHz.
- Overclocking to 250 MHz, the fastest speed was 40 kHz.

At higher speeds the frequency of GP2 just gets weird. It never gets much faster 
than 40 kHz, and sometime drops to about 1 kHz.

## Running the DAC with the PWM ISR
I tested long it took to compute the sine in the ISR and variations. Then 
I ran a loop that only did the computation, a quadratic approximation, and a 
LUT. For 250 MHz PicoW clock, the results were

| Method | us/loop |
|----|----|
|Compute| 35.2 |
|Approx 1| 68.5 |
|Approx 2 | 63.8 |
| LUT | 8.2 |

Clearly the LUT is the way to go.

The result was with the 250 MHz clock the max sample frequency was 6.4 kHz, so for a 
LUT with 32 entries, that give a signal frequency of 200 Hz.

**Disappointing**

## Trying a 12-bit I2C DAC
I switched to a 12-bit DAC. Same basic result.

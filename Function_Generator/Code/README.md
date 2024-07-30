# AstroHuster-Instrumentation_Lab-Code
- The file AWG_Sines.py is the MicroPython code that runs the function 
  generator. Use this code with the DAC PCB to generate a series of 
  sinusoids and collect data.

  The DAC is implemented with an R-2R resistor ladder. The PCB has a dual
  op amp. One half creates a virtual ground at 1/2 of 3.3V, the second is
  a follower to buffer the output of the resistor ladder

  The trick to getting a high-speed DAC to work is to use the low level
  `pio` and `dma` Pico features. This is an advanced non-python
  programming feature of the RP2040 processor on the Pico W.

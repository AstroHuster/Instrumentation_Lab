# AstroHuster ➡ Instrumentation_Lab ➡ Code

## The Design of the Function Generator

The DAC is implemented with an R-2R resistor ladder. The PCB has a dual op amp. One half creates a virtual ground at 1/2 of 3.3V, the second is a follower to buffer the output of the resistor ladder.

The DAC can be used by setting the pins `GP00` to `GP07` to high or low, with `GP07` the most significant digit. This creates an 8-bit DAC.

The trick to getting the DAC to work at high speed is to use the low level `pio` and `dma` Pico features. This is an advanced non-python programming feature of the RP2040 processor on the Pico W.

## Code for Pico W

This is the code for the Pico W on the Function Generator.
- `testDAC.py` - This code slowly sets the DAC to every step in its resolution, then uses the ADC to read and print the DAC value, the Signal, the Virtual Ground and the Signal relative to the Virtual Ground. This data can be plotted to measure the linearity of the DAC. It can be run in both the 8-bit and 4-bit mode.
- `AWG_Sines.py` - The MicroPython code that runs the Function Generator in the Sine mode. This code steps the ouput through a series of frequencies the user input. The spacing can be linear or logarithmic..

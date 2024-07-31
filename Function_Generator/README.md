# astrohuster-Instrumentation_Lab-Function_Generator
## The Design of the Function Generator

The DAC is implemented with an R-2R resistor ladder. The PCB has a dual op amp. One half creates a virtual ground at 1/2 of 3.3V, the second is a follower to buffer the output of the resistor ladder.

The DAC can be used by setting the pins `GP00` to `GP07` to high or low, with `GP07` the most significant digit. This creates an 8-bit DAC.

The trick to getting the DAC to work at high speed is to use the low level `pio` and `dma` Pico features. This is an advanced non-python programming feature of the RP2040 processor on the Pico W.

# Code
The code for the Function Generator is in the folder Code

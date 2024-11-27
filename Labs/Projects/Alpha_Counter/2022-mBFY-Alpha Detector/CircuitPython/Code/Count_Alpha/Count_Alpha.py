"""
Count_Alpha.py
Uses the countio module on the AdaFruit Feather ESP32S2 TFT to
count alpha particles detected with a S1223 photodiode and
processed with a MCP 6022 op amp.

ProfHuster@gmail.com
2022-03-25

22b: No LED. Light contamination!
"""
import time
import board
import countio
from digitalio import DigitalInOut, Direction

print("# Count_Alpha")
counterPin = board.IO5 # Any IO pin will work
nPrint = 100 # how often to print label
reportTime = int(1) # in seconds
# Use the monotonic_ns counter
# Note the "_" in number is like a comma when writing
reportNanos = 1_000_000_000 * reportTime

# LED pin
pLED = DigitalInOut(board.LED)
pLED.direction = Direction.OUTPUT
pLED.value = 0

# Set stop time for loop
stopNanos  = time.monotonic_ns() + reportNanos
# Set variables used in the loop
print(f"# Time (s), Counts, Avg Counts in {reportTime} seconds")
iPrint = 0
Total = 0
nLoops = 0

# Set up the counter
pin_counter = countio.Counter(counterPin)
# Reset counter and go
pin_counter.reset()

try:
    while True:
        # Wait until time is up
        while time.monotonic_ns() < stopNanos:
            time.sleep(0.001)
        # Calculate Counts per Minute
        counts = pin_counter.count
        # Reset counter
        pin_counter.reset()

        Total += counts
        nLoops += 1
        iPrint += 1
        if iPrint >= nPrint:
            iPrint = 0
            print(f"# Time (s), Counts, Avg Counts in {reportTime} seconds")
        # Set next report time
        stopNanos += reportNanos
        print(f"{time.monotonic():10.0f}, {counts:6d}, {Total/nLoops:.3f}")
except:
    pin_counter.deinit()

# EOF End Of File
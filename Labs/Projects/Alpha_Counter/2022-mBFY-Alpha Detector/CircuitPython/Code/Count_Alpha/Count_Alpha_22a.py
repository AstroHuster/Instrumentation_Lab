"""
Count_Alpha_22a.py
Uses the countio module on the AdaFruit Feather ESP32S2 TFT to
count alpha particles detected with a S1223 photodiode and
processed with a MCP 6022 op amp.

ProfHuster@gmail.com
2022-03-25
"""
import time
import board
import countio
from digitalio import DigitalInOut, Direction

print("# Count_Alpha")
reportTime = int(1) # in seconds
counterPin = board.IO5 # Any IO pin will work
nPrint = 100 # how often to print label

# Use the monotonic_ns counter
# Note the "_" in number is like a comma when writing
reportNanos = 1_000_000_000 * reportTime

# LED pin
pLED = DigitalInOut(board.LED)
pLED.direction = Direction.OUTPUT

# Set up the counter
pin_counter = countio.Counter(counterPin)

# Set stop time for loop
stopNanos  = time.monotonic_ns() + reportNanos

print(f"# Time (s), Counts, Avg Counts in {reportTime} seconds")
iPrint = 0
# Reset counter and go
pin_counter.reset()

Total = 0
nLoops = 0
while True:
    # Wait until time is up
    while time.monotonic_ns() < stopNanos:
        time.sleep(0.001)
    # Calculate Counts per Minute
    counts = pin_counter.count
    Total += counts
    nLoops += 1
    # Reset counter
    pin_counter.reset()
    iPrint += 1
    if iPrint >= nPrint:
        iPrint = 0
        print(f"# Time (s), Counts, Avg Counts in {reportTime} seconds")
    # Set next report time
    stopNanos += reportNanos
    print(f"{time.monotonic():10.0f}, {counts:6d}, {Total/nLoops:.3f}")
    # Toggle the LED
    pLED.value = not pLED.value

# EOF End Of File
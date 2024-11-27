import board
import countio
from time import sleep

print("# testCountio")

# Count rising edges only.
pin_counter = countio.Counter(board.D5, edge=countio.Edge.FALL)
print(pin_counter.count)
# Reset the count after 100 counts.
totalCounts = 0
nLoops = 0
try:
    while True:
        sleep(1)
        nLoops += 1
        counts = pin_counter.count
        totalCounts += counts
        # pin_counter.reset()
        print(counts, totalCounts / nLoops)
except:
    print("# EXCEPTION")
    pin_counter.deinit()
# EOF
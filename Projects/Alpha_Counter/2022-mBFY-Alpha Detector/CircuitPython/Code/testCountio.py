import board
import countio
import digitalio
from time import sleep

print("# testCountio")

try:
    # Count rising edges only.
    pin_counter = countio.Counter(board.IO5, \
                                  edge=countio.Edge.RISE) #\
#                                  ,pull=digitalio.Pull.DOWN)
    pin_counter.reset()
    print(pin_counter.count)

    oldCounts = 0
    nLoops = 0
    pin_counter.reset()
    while True:
        sleep(1)
        nLoops += 1
        counts = pin_counter.count
        newCounts = counts - oldCounts
        oldCounts = counts
        # pin_counter.reset()
        print(nLoops, newCounts, counts / nLoops)
except:
    print("# EXCEPTION")
    pin_counter.deinit()
# EOF
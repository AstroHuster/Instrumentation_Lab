""" FIF0.py
Use a list and append and pop(0) to make a First In First Out queue.
Notes:
- if you try to push more than n items, the oldest are silently discarded.

ProfHuster@GMail.com
2024-10-31
"""

class FIFO:
    def __init__(self, n=16):
        self.n = n
        # Initially fill with floating zeros
        self.fifo = []
    def push(self, x):
        self.fifo.append(x)
        while len(self.fifo) > self.n:
            self.fifo.pop(0)
    def pop(self):
        # If you pop and empty list, raises IndexError
        return self.fifo.pop(0)

if __name__ == "__main__":
    fifo = FIFO(5)
    for i in range(7):
        fifo.push(float(i))
        print(fifo.fifo)

    for i in range(6):
        x = fifo.pop()
        print(x, fifo.fifo)

# END
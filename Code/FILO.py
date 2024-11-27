
class FILO:
    def __init__(self, n=16):
        self.n = n
        self.first = 0 
        self.last = 0
        self.filo = self.n * [None]
    def push(self, x):
        self.filo[self.first] = x
        self.first = (self.first+1) % self.n
    def pop(self):
        x = self.filo[self.last]
        self.filo[self.last] = None 
        self.last = (self.last + 1) % self.n
        return x

filo = FILO(16)
for i in range(8):
    filo.push(i)
    print(filo.filo)

for i in range(17):
    x = filo.pop()
    if x:
        print(x)
        print(filo.filo)
    else:
        print("FILO EMPTY")

# END
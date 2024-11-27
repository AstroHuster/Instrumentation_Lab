""" running_avg_std.py
Use a FIFO to compute running average and standard deviation.

ProfHuster@GMail.com
2024-10-31
"""
from math import sqrt
from FIFO import FIFOak

i_data = -1
def read_data():
    global i_data
    i_data += 1
    return(i_data)

N_FIFO = 10
fifo = FIFO(N_FIFO)

sum_avg = 0.0
sum_sq = 0.0

# Fill fifo to start
# Start the sum and sum of squares
for i in range(N_FIFO):
    x = read_data()
    sum_avg += x
    sum_sq += x**2
    fifo.push(x)
    
avg = sum_avg / N_FIFO
std = sqrt(sum_sq / N_FIFO - avg**2)
print(f"Starting:\n    avg,    std\n{avg:7.2f}, {std:7.2f}")

# Now keep pushing numbers and compute running average

for i in range(N_FIFO, 2*N_FIFO):
    # print(fifo.fifo)
    # Pop oldest number
    x_old = fifo.pop()
    # Subtract it and its square from their sums
    sum_avg -= x_old
    sum_sq -= x_old**2
    
    # Push new number
    x_new = float(i)
    fifo.push(x_new)

    # Add it and its square to their sums
    sum_avg += x_new
    sum_sq += x_new**2

    # Calculate avg and std
    avg = sum_avg / N_FIFO
    std = sqrt(sum_sq / N_FIFO - avg**2)

    print(f"{avg:7.2f}, {std:7.2f}")


# END
cmp1 = complex(input("Enter complex (or real) number: "))
print("cmp1 = ", cmp1)

cmp2 = complex(input("Enter complex (or real) number: "))
print("cmp2 = ", cmp2)
print("cmp1 + cmp2 = ", cmp1 + cmp2)
print("cmp1 * cmp2 = ", cmp1 * cmp2)
print("abs", cmp2, " = ", abs(cmp2))

# Get disk size and free space

import os

(blksize, fragsize, nblocks, nfree, _, _, _, _, _, _) = os.statvfs('/')

print(f"There are {blksize*nblocks} bytes, {blksize*nfree} bytes are available.")

with open("data", 'w') as fp:
    for i in range(1000):
        fp.write(" ")


(blksize, fragsize, nblocks, nfree, _, _, _, _, _, _) = os.statvfs('/')

print(f"There are {blksize*nblocks} bytes, {blksize*nfree} bytes are available.")

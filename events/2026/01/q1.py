import sys
from math import isqrt

needed: int = 0

with open(sys.argv[1], "r") as file:
    for line in file:
        numbers = list(map(int, line.split(",")))
        for c in numbers:
            s = isqrt(c)
            if s * s < c:
                needed += (s + 1) * (s + 1) - c

print(needed)

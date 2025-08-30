from collections.abc import Iterator
from itertools import dropwhile
import numpy as np


def input(part: int) -> int:
    with open(f"everybody_codes_e2024_q08_p{part}.txt", "r") as file:
        return int(file.readline())


def p3_blocks_generator(priests: int, acolytes: int) -> Iterator[int]:
    s = np.array([1])
    t = 1
    yield s.sum()
    while True:
        # compute the new structure
        t = (t * priests) % acolytes + acolytes
        s = np.concatenate((np.array([t]), t + s, np.array([t])))
        # Figure out how many bottom blocks we can remove
        bottom_blocks = np.sum((s[1:-1] * len(s) * priests) % acolytes)
        yield s.sum() - bottom_blocks


# Part 1
P1_BLOCKS = input(1)

p1_blocks, total_p1_blocks = 1, 1
while total_p1_blocks < P1_BLOCKS:
    p1_blocks += 2
    total_p1_blocks += p1_blocks
print(f"Part 1: Product is {p1_blocks * (total_p1_blocks - P1_BLOCKS)}")

# # Part 2
P2_ACOLYTES = 1111
P2_BLOCKS = 20240000
P2_PRIESTS = input(2)

p2_blocks = 1
p2_thickness = 1
p2_width = 1
while p2_blocks < P2_BLOCKS:
    p2_width += 2
    p2_thickness *= P2_PRIESTS
    p2_thickness %= P2_ACOLYTES
    p2_blocks += p2_thickness * p2_width

print(f"Part 2: Product is {p2_width * (p2_blocks - P2_BLOCKS)}")

# Part 3
P3_BLOCKS = 202400000
P3_PRIESTS = input(3)
P3_ACOLYTES = 10

p3_blocks_stream = p3_blocks_generator(P3_PRIESTS, P3_ACOLYTES)
b = next(
    dropwhile(lambda x: x < P3_BLOCKS, p3_blocks_generator(P3_PRIESTS, P3_ACOLYTES))
)
print(f"Part 3: Buy {b - P3_BLOCKS} blocks.")

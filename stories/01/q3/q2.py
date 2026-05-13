from dataclasses import dataclass
from math import lcm
import re
import sys


@dataclass
class Snail:
    x: int
    y: int

    def __post_init__(self) -> None:
        self.period = self.x + self.y - 1

    @property
    def offset(self) -> int:
        return self.y - 1

    @property
    def score(self) -> int:
        return self.x + 100 * self.y

    def advance(self, n: int = 1) -> None:
        n %= self.period
        for _ in range(n):
            if self.y == 1:
                self.x = 1
                self.y = self.period
            else:
                self.x += 1
                self.y -= 1


snails: list[Snail] = []

with open(sys.argv[1], "r") as file:
    for line in file:
        m = re.match(r"x=(\d+) y=(\d+)", line)
        assert m is not None
        snails.append(Snail(int(m.group(1)), int(m.group(2))))

current_period: int = snails[0].period
current_offset: int = snails[0].offset

for s in snails[1:]:
    new_offset: int = current_offset
    s.advance(current_offset)
    while s.offset != 0:
        s.advance(current_period)
        new_offset += current_period
    current_period = lcm(current_period, s.period)
    current_offset = new_offset

print(current_offset)

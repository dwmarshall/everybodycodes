from dataclasses import dataclass
import re
import sys


@dataclass
class Snail:
    x: int
    y: int

    def __post_init__(self) -> None:
        self.disc = self.x + self.y - 1

    @property
    def score(self) -> int:
        return self.x + 100 * self.y

    def advance(self, n: int = 1) -> None:
        n %= self.disc
        for _ in range(n):
            if self.y == 1:
                self.x = 1
                self.y = self.disc
            else:
                self.x += 1
                self.y -= 1


snails: list[Snail] = []

with open(sys.argv[1], "r") as file:
    for line in file:
        m = re.match(r"x=(\d+) y=(\d+)", line)
        assert m is not None
        snails.append(Snail(int(m.group(1)), int(m.group(2))))

total_score: int = 0

for s in snails:
    s.advance(100)
    total_score += s.score

print(f"Total score is {total_score}")

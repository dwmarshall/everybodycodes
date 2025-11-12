from __future__ import annotations
from dataclasses import dataclass
from math import inf


@dataclass
class Segment:
    id: int | None = None
    spine: int | None = None
    left: int | None = None
    right: int | None = None
    next: Segment | None = None

    # def __lt__(self, other: Segment) -> bool:
    #     if self.quality() < other.quality():
    #         return True

    def add(self, n: int) -> None:
        if self.spine is None:
            self.spine = n
        elif n < self.spine and self.left is None:
            self.left = n
        elif n > self.spine and self.right is None:
            self.right = n
        else:
            if self.next is None:
                self.next = Segment()
            self.next.add(n)

    def quality(self) -> str:
        if self.next is None:
            return str(self.spine)
        else:
            return str(self.spine) + self.next.quality()

    def level_scores(self) -> list[int]:
        if self.spine is None:
            return [0]
        this_level = int(str(self.left or "") + str(self.spine) + str(self.right or ""))
        if self.next is None:
            return [this_level]
        else:
            return [this_level] + self.next.level_scores()


def input(n: int, testing: bool = False) -> list[tuple[int, list[int]]]:
    filename = f"test{n}.txt" if testing else f"everybody_codes_e2025_q05_p{n}.txt"
    lines: list[tuple[int, list[int]]] = []
    with open(filename) as file:
        for line in file:
            id, numbers = line.split(":")
            lines.append((int(id), list(map(int, numbers.split(",")))))
    return lines


fishbone = Segment()

for _, sword in input(1):
    for q in sword:
        fishbone.add(q)

print(f"Part 1: {fishbone.quality()}")

# Part 2
min_quality, max_quality = inf, -inf

for _, sword in input(2):
    fishbone = Segment()
    for q in sword:
        fishbone.add(q)
    result = int(fishbone.quality())
    min_quality = min(min_quality, result)
    max_quality = max(max_quality, result)

print(f"Part 2: Difference is {max_quality - min_quality}")

# Part 3

from __future__ import annotations
from dataclasses import dataclass
from math import inf


@dataclass
class Segment:
    spine: int | None = None
    left: int | None = None
    right: int | None = None
    next: Segment | None = None

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


@dataclass
class Sword:
    id: int
    head: Segment

    def __init__(self, id: int, values: list[int]):
        self.id = id
        self.head = Segment()
        for v in values:
            self.head.add(v)

    def quality(self) -> int:
        result = ""
        curr = self.head
        while curr is not None:
            result += str(curr.spine)
            curr = curr.next
        return int(result)

    def level_scores(self) -> list[int]:
        scores: list[int] = []
        curr = self.head
        while curr is not None:
            this_level = (
                str(curr.left or "") + str(curr.spine or "") + str(curr.right or "")
            )
            scores.append(int(this_level) or 0)
            curr = curr.next
        return scores

    def __lt__(self, other: Sword) -> bool:
        return (self.quality(), self.level_scores(), self.id) < (
            other.quality(),
            other.level_scores(),
            other.id,
        )


def input(n: int, testing: bool = False) -> list[tuple[int, list[int]]]:
    filename = f"test{n}.txt" if testing else f"everybody_codes_e2025_q05_p{n}.txt"
    lines: list[tuple[int, list[int]]] = []
    with open(filename) as file:
        for line in file:
            id, numbers = line.split(":")
            lines.append((int(id), list(map(int, numbers.split(",")))))
    return lines


for id, values in input(1):
    sword = Sword(id, values)
    print(f"Part 1: {sword.quality()}")


# Part 2
min_quality, max_quality = inf, -inf

for id, values in input(2):
    sword = Sword(id, values)
    result = sword.quality()
    min_quality = min(min_quality, result)
    max_quality = max(max_quality, result)

print(f"Part 2: Difference is {max_quality - min_quality}")

# Part 3

swords: list[Sword] = []

for id, values in input(3):
    swords.append(Sword(id, values))

swords.sort(reverse=True)

checksum = 0
for i, s in enumerate(swords):
    checksum += (i + 1) * s.id

print(f"Part 3: Checksum is {checksum}")

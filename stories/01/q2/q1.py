from __future__ import annotations
from collections import defaultdict, deque
from dataclasses import dataclass
import re
import sys
from typing import Generator


@dataclass
class Tree:
    value: int
    label: str
    left: Tree | None = None
    right: Tree | None = None

    def add(self, other: Tree) -> int:
        level = 0
        curr: Tree = self

        while True:
            assert other.value != curr.value
            if other.value < curr.value:
                if curr.left is None:
                    curr.left = other
                    return level + 1
                curr = curr.left
            else:
                if curr.right is None:
                    curr.right = other
                    return level + 1
                curr = curr.right
            level += 1

    def extract(self) -> str:
        entries: dict[int, list[str]] = defaultdict(list)
        q: deque[tuple[Tree, int]] = deque([(self, 0)])

        while q:
            node, level = q.popleft()
            entries[level].append(node.label)
            if node.left:
                q.append((node.left, level + 1))
            if node.right:
                q.append((node.right, level + 1))

        result = sorted(entries.values(), key=len, reverse=True)[0]
        return "".join(result)

    def swap(self, other: Tree) -> None:
        self.value, other.value = other.value, self.value
        self.label, other.label = other.label, self.label
        # For Part 2, don't swap the subtrees
        # self.left, other.left = other.left, self.left
        # self.right, other.right = other.right, self.right


def input() -> Generator[tuple[str, int, Tree, Tree] | tuple[str, int]]:

    with open(sys.argv[1], "r") as file:
        lines = file.readlines()
        for line in lines:
            if m := re.match(
                r"ADD id=(\d+) left=\[(\d+),(.)\] right=\[(\d+),(.)\]", line
            ):
                yield (
                    "ADD",
                    int(m.group(1)),
                    Tree(int(m.group(2)), m.group(3)),
                    Tree(int(m.group(4)), m.group(5)),
                )
            elif m := re.match(r"SWAP (\d+)", line):
                yield ("SWAP", int(m.group(1)))


left_lookup: dict[int, Tree] = {}
right_lookup: dict[int, Tree] = {}

left: Tree | None = None
right: Tree | None = None

for t in input():
    if t[0] == "ADD" and len(t) == 4:
        id = t[1]
        input_left, input_right = t[2:]
        left_lookup[id] = input_left
        right_lookup[id] = input_right
        if left is None:
            left = input_left
        else:
            left.add(input_left)

        if right is None:
            right = input_right
        else:
            right.add(input_right)
    elif t[0] == "SWAP" and len(t) == 2:
        left_swap: Tree = left_lookup[t[1]]
        right_swap: Tree = right_lookup[t[1]]
        left_swap.swap(right_swap)


assert left is not None and right is not None
print(left.extract() + right.extract())

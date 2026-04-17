from __future__ import annotations
from collections import defaultdict, deque
from dataclasses import dataclass
import re
import sys
from typing import Generator


@dataclass
class Node:
    value: int
    label: str
    left: Node | None = None
    right: Node | None = None

    def add(self, other: Node) -> int:
        level = 0
        curr: Node = self

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
        q: deque[tuple[Node, int]] = deque([(self, 0)])

        while q:
            node, level = q.popleft()
            entries[level].append(node.label)
            if node.left:
                q.append((node.left, level + 1))
            if node.right:
                q.append((node.right, level + 1))

        result = sorted(entries.values(), key=len, reverse=True)[0]
        return "".join(result)


def input() -> Generator[tuple[Node, Node]]:

    with open(sys.argv[1], "r") as file:
        lines = file.readlines()
        for line in lines:
            m = re.match(r"ADD id=\d+ left=\[(\d+),(.)\] right=\[(\d+),(.)\]", line)
            assert m is not None
            yield (
                Node(int(m.group(1)), m.group(2)),
                Node(int(m.group(3)), m.group(4)),
            )


left: Node | None = None
right: Node | None = None

for input_left, input_right in input():
    if left is None:
        left = input_left
    else:
        left.add(input_left)

    if right is None:
        right = input_right
    else:
        right.add(input_right)

assert left is not None and right is not None
print(left.extract() + right.extract())

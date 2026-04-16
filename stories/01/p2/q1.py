from __future__ import annotations
from collections import Counter, deque
from dataclasses import dataclass
import re
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

    def nodes_at_level(self, level: int) -> str:
        result = ""
        queue: deque[tuple[Node, int]] = deque([(self, 0)])

        while queue:
            node, node_level = queue.popleft()
            if node_level == level:
                result += node.label
            if node.left:
                queue.append((node.left, node_level + 1))
            if node.right:
                queue.append((node.right, node_level + 1))

        return result


def input(n: int, testing: bool = False) -> Generator[tuple[Node, Node]]:
    filename = f"test{n}.txt" if testing else f"everybody_codes_e1_q02_p{n}.txt"

    with open(filename, "r") as file:
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
left_counter: Counter[int] = Counter()
right_counter: Counter[int] = Counter()

for input_left, input_right in input(1):
    if left is None:
        left = input_left
        left_counter[0] += 1
    else:
        left_counter[left.add(input_left)] += 1

    if right is None:
        right = input_right
        right_counter[0] += 1
    else:
        right_counter[right.add(input_right)] += 1

most_numerous_left = left_counter.most_common(1)[0][0]
most_numerous_right = right_counter.most_common(1)[0][0]
assert left is not None and right is not None
print(
    left.nodes_at_level(most_numerous_left) + right.nodes_at_level(most_numerous_right)
)

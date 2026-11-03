import re
import sys
from collections import defaultdict

patt = re.compile(r"(\d+)([\<\>])(\d+)")

total: int = 0

with open(sys.argv[1], "r") as file:
    for line in file:
        outgoing: dict[str, set[str]] = defaultdict(set)
        incoming: dict[str, int] = defaultdict(int)
        for m in re.finditer(patt, line):
            # left is harder than right
            left, op, right = m[1], m[2], m[3]
            if op == "<":
                left, right = right, left
            outgoing[left].add(right)
            incoming[left] += 0  # so we know there's an entry for it
            incoming[right] += 1
        # make sure that all of the implied hardness is considered:
        for o in outgoing.values():
            for e in o:
                if e not in o:
                    o.add(e)
                    incoming[e] += 1

        result: list[str] = []
        while incoming:
            winner = next(k for k, v in incoming.items() if v == 0)
            result.append(winner)
            for edge in outgoing[winner]:
                incoming[edge] -= 1
            del incoming[winner]
            del outgoing[winner]
        checksum = int("".join(result))
        total += checksum
    print(total)

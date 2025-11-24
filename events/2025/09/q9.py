from collections import defaultdict
from itertools import combinations


def input(n: int, testing: bool = False) -> dict[int, str]:
    filename = f"test{n}.txt" if testing else f"everybody_codes_e2025_q09_p{n}.txt"
    result: dict[int, str] = {}
    with open(filename) as file:
        for s in file:
            id, _, genome = s.partition(":")
            result[int(id)] = genome.strip()
    return result


def related(a: str, b: str, c: str) -> bool:
    for i in range(len(c)):
        if a[i] != c[i] and b[i] != c[i]:
            return False
    return True


def similarity(a: str, b: str, c: str) -> int:
    a_hits = 0
    b_hits = 0
    for i in range(len(c)):
        if a[i] == c[i]:
            a_hits += 1
        if b[i] == c[i]:
            b_hits += 1
    return a_hits * b_hits


class UnionFind:
    def __init__(self, keys: list[int]):
        self.root = {k: k for k in keys}

    def find(self, x: int) -> int:
        if x == self.root[x]:
            return x
        self.root[x] = self.find(self.root[x])
        return self.root[x]

    def union(self, x: int, y: int) -> None:
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            self.root[rootY] = rootX

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)


# Part 1
family = input(1)
print(f"Part 1: similarity is {similarity(family[1], family[2], family[3])}")

# Part 2
family = input(2)
total_similarity = 0

unmatched_children = set(family.keys())

while unmatched_children:
    u_id = unmatched_children.pop()
    u = family[u_id]
    for s_id, t_id in combinations(family.keys(), 2):
        if u_id in (s_id, t_id):
            continue
        s = family[s_id]
        t = family[t_id]
        if related(s, t, u):
            total_similarity += similarity(s, t, u)
            break

print(f"Part 2: Total similarity is {total_similarity}")

# Part 3
family = input(3)
uf = UnionFind(list(family.keys()))

unmatched_children = set(family.keys())
while unmatched_children:
    u_id = unmatched_children.pop()
    u = family[u_id]
    for s_id, t_id in combinations(family.keys(), 2):
        if u_id in (s_id, t_id):
            continue
        s = family[s_id]
        t = family[t_id]
        if related(s, t, u):
            uf.union(s_id, u_id)
            uf.union(t_id, u_id)
            break

scale_numbers: dict[int, list[int]] = defaultdict(list)
for fam_id in family.keys():
    scale_numbers[uf.find(fam_id)].append(fam_id)

max_family = (0, 0)
for k in scale_numbers:
    this_family = (len(scale_numbers[k]), sum(scale_numbers[k]))
    max_family = max(max_family, this_family)

print(f"Part 3: The biggest family scale is {max_family[1]}")

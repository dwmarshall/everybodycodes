from itertools import combinations, pairwise


def input(n: int, testing: bool = False) -> list[int]:
    filename = f"test{n}.txt" if testing else f"everybody_codes_e2025_q08_p{n}.txt"
    with open(filename) as file:
        return list(map(int, file.readline().split(",")))


def intersects(string1: tuple[int, int], string2: tuple[int, int]) -> bool:
    s1 = sorted(string1)
    if set(string1) & set(string2):
        return False
    left_index = [x for x in string2 if s1[0] < x < s1[1]]
    return len(left_index) == 1


def cuts(pattern: list[tuple[int, int]], cut: tuple[int, int]) -> int:
    total_cuts = 0
    if cut in pattern:
        total_cuts += 1
    if tuple(reversed(cut)) in pattern:
        total_cuts += 1
    for t in pattern:
        if intersects(t, cut):
            total_cuts += 1
    return total_cuts


numbers = input(1)
pairs = 0

for x, y in pairwise(numbers):
    if abs(x - y) == 16:
        pairs += 1

print(f"Part 1: {pairs} pairs")

# Part 2

numbers = input(2)
knots = 0

strings: list[tuple[int, int]] = []

for x, y in pairwise(numbers):
    for t in strings:
        if intersects(t, (x, y)):
            knots += 1
    strings.append((x, y))

print(f"Part 2: Number of knots is {knots}")

# Part 3
numbers = input(3)
max_cuts = 0

strings: list[tuple[int, int]] = []

for x, y in pairwise(numbers):
    strings.append((x, y))

for t in combinations(range(1, 257), 2):
    this_cut = cuts(strings, t)
    max_cuts = max(max_cuts, this_cut)

print(f"Part 3: Max cuts is {max_cuts}")

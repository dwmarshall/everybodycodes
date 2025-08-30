from collections import Counter, deque
from itertools import count

COLUMNS = 4
P1_ROUNDS = 10


def clap(c: list[deque], curr: int) -> str:
    clapper = c[curr].popleft()
    new_col = (curr + 1) % len(c)
    pos = 0
    claps = 0
    direction = 1
    while True:
        claps += 1
        if claps == clapper:
            break
        pos += direction
        if pos == len(c[new_col]) or pos == -1:
            direction *= -1
            pos += direction

    if direction == 1:
        c[new_col].insert(pos, clapper)
    else:
        c[new_col].insert(pos + 1, clapper)
    return "".join(str(x[0]) for x in c)


def part1(c: list[deque]) -> str:
    current_col = 0

    for _ in range(P1_ROUNDS):
        last_shout = clap(c, current_col)
        current_col = (current_col + 1) % len(c)
    return last_shout


def part2(c: list[deque]) -> int:
    shouts = Counter()
    current_col = 0

    for i in count(1):
        shout = clap(c, current_col)
        shouts[shout] += 1
        if shouts[shout] == 2024:
            return int(shout) * i
        current_col = (current_col + 1) % len(c)


def part3(c: list[deque]) -> str:
    highest_number = ""
    current_col = 0
    for _ in range(100):
        shout = clap(c, current_col)
        highest_number = max(highest_number, shout)
        current_col = (current_col + 1) % len(c)
    return highest_number


parts = [None, part1, part2, part3]


for p in range(1, 4):
    with open(f"everybody_codes_e2024_q05_p{p}.txt", "r") as file:
        columns = [deque() for _ in range(COLUMNS)]
        for line in file:
            nums = list(map(int, line.split()))
            for i, n in enumerate(nums):
                columns[i].append(n)

    print(f"Part {p}: {parts[p](columns)}")

from collections.abc import Iterator
import math

FACTOR = {"A": 1, "B": 2, "C": 3}
TARGET_STRENGTH = {"H": 2, "T": 1}


def shot_path(catapult: tuple[int, int], power: int) -> Iterator[tuple[int, int]]:
    i, j = catapult
    for _ in range(power):
        i, j = i - 1, j + 1
        yield i, j
    for _ in range(power):
        j += 1
        yield i, j
    while i < ground_level:
        i, j = i + 1, j + 1
        yield i, j


# Parts 1 and 2

for p in range(1, 3):

    catapult = dict()
    targets = dict()
    with open(f"everybody_codes_e2024_q12_p{p}.txt", "r") as file:
        for i, line in enumerate(file):
            for j, c in enumerate(line):
                if c in "HT":
                    targets[(i, j)] = c
                elif c in "ABC":
                    catapult[c] = (i, j)
                elif c == "=":
                    ground_level = i
                    break

    ranking = {x: math.inf for x in targets}

    power = 1
    while any(x == math.inf for x in ranking.values()):
        for c, multiplier in FACTOR.items():
            for ij in shot_path(catapult[c], power):
                if ij in targets:
                    ranking[ij] = min(ranking[ij], power * multiplier)
        power += 1

    total_ranking = 0
    for target, target_type in targets.items():
        total_ranking += ranking[target] * TARGET_STRENGTH[target_type]

    print(f"Part {p}: Ranking value is {total_ranking}")

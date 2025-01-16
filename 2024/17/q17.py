from functools import reduce
from itertools import product
import math
import operator


def distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def input(n: int, testing: bool = False) -> list[tuple[int, int]]:
    stars = []

    filename = f"test{n}.txt" if testing else f"everybody_codes_e2024_q17_p{n}.txt"
    with open(filename, "r") as file:
        for i, line in enumerate(file):
            for j, c in enumerate(line):
                if c == "*":
                    stars.append((i, j))
    return stars


def constellations(
    sky: list[tuple[int, int]], max_distance: int = math.inf
) -> list[int]:
    results = []

    unvisited = set(sky)

    while unvisited:
        this_constellation = {unvisited.pop()}
        constellation_mst = 0
        while True:
            weights = []
            for u, v in product(unvisited, this_constellation):
                if (d := distance(u, v)) >= max_distance:
                    continue
                weights.append((d, u))
            if weights:
                weights.sort()
                constellation_mst += weights[0][0]
                unvisited.remove(weights[0][1])
                this_constellation.add(weights[0][1])
            else:
                results.append(constellation_mst + len(this_constellation))
                break
    assert len(unvisited) == 0

    return sorted(results, reverse=True)


# Parts 1 and 2
for p in range(1, 3):
    sky = input(p)

    results = constellations(sky)
    assert len(results) == 1

    print(f"Part {p}: The lowest size is {results[0]}")

# Part 3
sky = input(3)
results = constellations(sky, 6)
answer = reduce(operator.__mul__, results[:3])
print(f"Part 3: The product is {answer}")

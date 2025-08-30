from functools import reduce
import heapq
import math
import operator

DIRECTIONS = {
    "U": (0, 0, 1),
    "D": (0, 0, -1),
    "F": (0, 1, 0),
    "B": (0, -1, 0),
    "R": (1, 0, 0),
    "L": (-1, 0, 0),
}


class Plant:
    def __init__(self):
        self.tip = [0] * 3
        self.max_height = 0
        self.segments = set()

    def apply(self, instruction: str) -> None:
        direction, steps = instruction[:1], int(instruction[1:])
        growth = DIRECTIONS[direction]
        for _ in range(steps):
            for i in range(3):
                self.tip[i] += growth[i]
            self.segments.add(tuple(self.tip))
        self.max_height = max(self.max_height, self.tip[2])


def shortest_paths(
    g: set[tuple[int, int, int]], tips: set[tuple[int, int, int]]
) -> int:
    main_trunk = {x for x in g if x[0] == 0 and x[1] == 0}
    tip_lengths = dict()
    for t in tips:
        best_paths = {x: math.inf for x in main_trunk}
        visited = set()
        leaves = []
        heapq.heappush(leaves, (0, t))
        while leaves:
            steps, position = heapq.heappop(leaves)
            if position in visited:
                continue
            if steps > max(best_paths.values()):
                continue
            if position in best_paths:
                best_paths[position] = min(best_paths[position], steps)
            visited.add(position)
            x, y, z = position
            for dx, dy, dz in DIRECTIONS.values():
                nx, ny, nz = x + dx, y + dy, z + dz
                if (nx, ny, nz) in grid:
                    heapq.heappush(leaves, (steps + 1, (nx, ny, nz)))
        tip_lengths[t] = best_paths
    totals = {m: 0 for m in main_trunk}
    for m in main_trunk:
        for t in tips:
            totals[m] += tip_lengths[t][m]
    return min(totals.values())


for p in range(1, 4):
    plants = []

    with open(f"everybody_codes_e2024_q14_p{p}.txt", "r") as file:
        for line in file:
            new_plant = Plant()
            for instruction in line.strip().split(","):
                new_plant.apply(instruction)
            plants.append(new_plant)

    assert p != 1 or len(plants) == 1

    if p == 1:
        print(f"Part 1: The maximum height is {plants[0].max_height}")
    elif p == 2:
        total_segments = reduce(operator.__or__, [x.segments for x in plants])
        print(f"Part 2: The total segments are {len(total_segments)}")
    elif p == 3:
        grid = reduce(operator.__or__, [x.segments for x in plants])
        tips = set(tuple(x.tip) for x in plants)
        print(f"Part 3: Minimum murkiness is {shortest_paths(grid, tips)}")

import heapq
from math import inf

DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def input(
    n: int, testing: bool = False
) -> tuple[
    list[list[str]], set[tuple[int, int]], set[tuple[int, int]], set[tuple[int, int]]
]:
    grid = []
    palms = set()
    starts = set()
    desert = set()

    filename = f"test{n}.txt" if testing else f"everybody_codes_e2024_q18_p{n}.txt"
    with open(filename, "r") as file:
        for y, line in enumerate(file):
            grid.append(list(line.strip()))
            for x, c in enumerate(line.strip()):
                if c == ".":
                    desert.add((x, y))
                    if x == 0 or x == len(line) - 2:
                        starts.add((x, y))
                elif c == "P":
                    palms.add((x, y))

    return grid, palms, desert, starts


def solve(
    maze: list[list[str]],
    origins: list[tuple[int, int]],
    goals: list[tuple[int, int]],
    nte: int = None,
) -> list[int]:
    """Returns a list of the times for each tree to get water"""
    pq = []
    for x in origins:
        heapq.heappush(pq, (0, x))

    visited = set()
    watering_times = []

    while pq:
        steps, location = heapq.heappop(pq)
        if location in visited:
            continue
        visited.add(location)
        x, y = location
        if maze[y][x] == "P":
            goals.remove((x, y))
            watering_times.append(steps)
            if nte is not None and sum(watering_times) >= nte:
                return None
            if len(goals) == 0:
                return watering_times
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]) and maze[ny][nx] != "#":
                heapq.heappush(pq, (steps + 1, (nx, ny)))


for p in range(1, 3):
    field, palms, _, inlets = input(p)
    answer = solve(field, inlets, palms)
    print(f"Part {p}: It takes {answer[-1]} minutes")

# Part 3

field, palms, desert, _ = input(3)
best_total_time = inf

for well in desert:
    times = solve(field, {well}, palms.copy(), best_total_time)
    if times is not None:
        best_total_time = min(best_total_time, sum(times))

print(f"Part 3: The best sum is {best_total_time}")

from collections import defaultdict
from functools import cache
from itertools import pairwise
import heapq
import string

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def input(
    part: int, testing: bool = False
) -> tuple[tuple[tuple[str]], tuple[int, int], dict[str, tuple[int, int]]]:
    filename = (
        f"test{part}.txt" if testing else f"everybody_codes_e2024_q15_p{part}.txt"
    )
    grid = []
    herbs = dict()

    with open(filename, "r") as file:
        for line in file:
            grid.append(tuple(line.strip()))

    starting_position = grid[0].index("."), 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] in string.ascii_uppercase:
                herbs[(j, i)] = grid[i][j]

    return tuple(grid), starting_position, herbs


def path_length(g: tuple[tuple[str]], path: tuple[tuple[int, int]]) -> int:
    total_length = 0
    for a, b in pairwise(path):
        total_length += minimum_steps(g, a, b)
    return total_length


def remaining_herbs(
    g: tuple[tuple[str]], h: dict[tuple[int, int], str], path: tuple[tuple[int, int]]
) -> set[str]:
    herbs = set(h.values())
    for p in path:
        x, y = p
        if g[y][x] in herbs:
            herbs.remove(g[y][x])
    return herbs


def solve(
    g: tuple[tuple[str]], h: dict[tuple[int, int], str], origin: tuple[int, int]
) -> int:
    q = []
    initial_state = (
        origin,  # position
        frozenset(),  # herbs acquired
    )
    visited = defaultdict(lambda: float("inf"))
    least_steps = float("inf")
    heapq.heappush(q, (0, 0, initial_state))
    while q:
        # print(len(q), least_steps, q[0])
        _, steps, state = heapq.heappop(q)
        if steps > visited[state]:
            continue
        (x, y), herbs_acquired = state
        if (x, y) == origin and herbs_acquired == frozenset(h.values()):
            least_steps = min(least_steps, steps)
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(g) and 0 <= nx < len(g[0]) and g[ny][nx] not in "#~":
                new_herbs_acquired = herbs_acquired
                if (nx, ny) in h:
                    new_herbs_acquired = herbs_acquired | {h[(nx, ny)]}
                state = ((nx, ny), frozenset(new_herbs_acquired))
                if steps + 1 < visited[state]:
                    visited[state] = steps + 1
                    heapq.heappush(
                        q,
                        (-len(new_herbs_acquired), steps + 1, state),
                    )
    return least_steps


@cache
def minimum_steps(
    g: tuple[tuple[str]], start_at: tuple[int, int], end_at: tuple[int, int]
) -> int:
    visited = set()
    q = []
    heapq.heappush(q, (0, start_at))
    while q:
        steps, current_position = heapq.heappop(q)
        if current_position == end_at:
            return steps
        if current_position in visited:
            continue
        visited.add(current_position)
        x, y = current_position
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(g) and 0 <= nx < len(g[0]) and g[ny][nx] not in "#~":
                heapq.heappush(q, (steps + 1, (nx, ny)))


for p in range(1, 4):
    maze, start, herbs = input(p)
    print(f"Part {p}: minimum steps are {solve(maze, herbs, start)}")

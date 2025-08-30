from collections import defaultdict
import heapq
import math

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def input(
    part: int, testing: bool = False
) -> tuple[dict[int, dict[int, int]], list[int], int]:
    point_level = dict()
    point_index = dict()
    S = []

    filename = "test.txt" if testing else f"everybody_codes_e2024_q13_p{part}.txt"
    with open(filename, "r") as file:
        for y, line in enumerate(file):
            for x, c in enumerate(line.strip()):
                if c not in "# ":
                    if c == "S":
                        i = point_index[(x, y)] = len(point_index)
                        S.append(i)
                        point_level[(x, y)] = 0
                    elif c == "E":
                        i = point_index[(x, y)] = len(point_index)
                        E = i
                        point_level[(x, y)] = 0
                    else:
                        i = point_index[(x, y)] = len(point_index)
                        point_level[(x, y)] = int(c)

    graph = defaultdict(dict)
    for p in point_level:
        x, y = p
        i = point_index[(x, y)]
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if (nx, ny) in point_level:
                j = point_index[(nx, ny)]
                graph[i][j] = 1 + level_time(point_level[(x, y)], point_level[(nx, ny)])

    return graph, S, E


def level_time(a: int, b: int) -> int:
    a, b = sorted((a, b))
    times = [b - a, 10 + a - b]
    return min(times)


for p in range(1, 4):

    maze, starting_points, ending_at = input(p)

    distances = [math.inf] * (max(maze) + 1)
    distances[ending_at] = 0

    unvisited = set(maze.keys())
    q = []
    heapq.heappush(q, (0, ending_at))

    # It's somewhat distressing that it took so long to
    # understand that Dijkstra was the correct approach
    # to this problem.
    while unvisited:
        _, u = heapq.heappop(q)
        if u in unvisited:
            unvisited.remove(u)
            for v in maze[u]:
                distances[v] = min(distances[v], distances[u] + maze[u][v])
                heapq.heappush(q, (distances[v], v))

    best_time = min(distances[x] for x in starting_points)
    print(f"Part {p}: The minimum time is {best_time}")

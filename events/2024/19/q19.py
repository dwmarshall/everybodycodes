from collections import deque
import copy
from functools import cache
from itertools import cycle, product


def input(n: int, testing: bool = False) -> tuple[list[list[str]], str]:
    filename = f"test{n}.txt" if testing else f"everybody_codes_e2024_q19_p{n}.txt"

    grid = []

    with open(filename, "r") as file:
        message_key = file.readline().strip()
        assert len(file.readline().strip()) == 0
        for line in file:
            grid.append(list(line.strip()))

    return grid, message_key


LETTER_DIRECTIONS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
]


# L : -1, R: 1
def rotate(g: list[list[str]], i: int, j: int, steps: int) -> None:
    assert 0 < i < len(g) - 1
    assert 0 < j < len(g[0]) - 1
    letters = deque()
    for di, dj in LETTER_DIRECTIONS:
        letters.append(g[i + di][j + dj])
    letters.rotate(steps)
    for c, (di, dj) in zip(letters, LETTER_DIRECTIONS):
        g[i + di][j + dj] = c


def apply_key(m: list[list[tuple[int, int]]], key: str) -> None:

    rotation_points = product(range(1, len(m) - 1), range(1, len(m[0]) - 1))
    for (i, j), direction in zip(rotation_points, cycle(key)):
        rotate(m, i, j, -1 if direction == "L" else 1)


def apply_transform(
    m: list[list[object]], t: list[list[tuple[int, int]]]
) -> list[list[object]]:
    assert len(m) == len(t)
    assert len(m[0]) == len(t[0])
    t = copy.deepcopy(t)
    for i in range(len(m)):
        for j in range(len(m[0])):
            mi, mj = t[i][j]
            t[i][j] = m[mi][mj]
    return t


@cache
def transform(i: int, j: int, key: str, n: int) -> list[list[tuple[int, int]]]:
    """transform is a noun in this context"""
    matrix = [[(ii, jj) for jj in range(j)] for ii in range(i)]

    if n == 0:
        return matrix
    elif n == 1:
        apply_key(matrix, key)
        return matrix
    elif n % 2 == 0:
        intermediate = transform(i, j, key, n // 2)
        return apply_transform(intermediate, intermediate)
    else:
        single = transform(i, j, key, 1)
        multi = transform(i, j, key, n - 1)
        return apply_transform(single, multi)


def extract_message(m: list[list[str]]) -> str:
    for row in m:
        if ">" in row and "<" in row:
            left = row.index(">")
            right = row.index("<")
            return "".join(row[left + 1 : right])


# Part 1
grid, key = input(1)

p1_transform = transform(len(grid), len(grid[0]), key, 1)
while (message := extract_message([grid[1]])) is None:
    grid = apply_transform(grid, p1_transform)
print(f"Part 1: The message is {message}")

# Part 2
grid, key = input(2)
p2_transform = transform(len(grid), len(grid[0]), key, 100)
grid = apply_transform(grid, p2_transform)
message = extract_message(grid)
print(f"Part 2: The message is {message}")

# Part 3
grid, key = input(3)
p3_transform = transform(len(grid), len(grid[0]), key, 1048576000)
grid = apply_transform(grid, p3_transform)
message = extract_message(grid)
print(f"Part 3: The message is {message}")
# def p1_message(g: list[list[str]], key: str) -> str:
#     middle_line = len(g) // 2

#     iters = []
#     iters.append(cycle(range(1, len(g) - 1)))
#     iters.append(cycle(range(1, len(g[0]) - 1)))
#     iters.append(cycle(key))

#     while g[middle_line][0] != ">" or g[middle_line][-1] != "<":
#         i, j, direction = tuple(next(iter) for iter in iters)
#         rotate(g, i, j, -1 if direction == "L" else 1)

#     return "".join(g[middle_line][1:-1])


# def p2_message(g: list[list[str]], key: str, rounds: int) -> str:

#     for _ in range(rounds):
#         rotation_points = product(range(1, len(g) - 1), range(1, len(g[0]) - 1))
#         for (i, j), direction in zip(rotation_points, cycle(key)):
#             rotate(g, i, j, -1 if direction == "L" else 1)

#     for row in g:
#         if ">" in row:
#             left = row.index(">")
#             right = row.index("<")
#             return "".join(row[left + 1 : right])


# # Part 1
# p1_grid, p1_key = input(1)
# print(f"Part 1: The message is {p1_message(p1_grid, p1_key)}")

# # Part 2
# p2_grid, p2_key = input(2)
# print(f"Part 2: The message is {p2_message(p2_grid, p2_key, 100)}")

# Part 3
# p3_grid, p3_key = input(3)
# print(len(p3_key), len(p3_grid), len(p3_grid[0]))
# for i in range(len(p3_grid)):
#     for j in range(len(p3_grid[0])):
#         p3_grid[i][j] = (i, j)
# print(p3_grid)
# p2_message(p3_grid, p3_key, 2)
# print(p3_grid[0])

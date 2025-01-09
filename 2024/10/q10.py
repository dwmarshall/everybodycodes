from collections.abc import Callable, Iterator
from itertools import product


def runic_word(tile: list[list[str]]) -> str:
    output = [tile[i][j] for i in range(2, 6) for j in range(2, 6)]
    return "".join(output)


def word_power(s: str) -> int:
    total_power = 0
    for i, c in enumerate(s):
        total_power += (i + 1) * (1 + ord(c) - ord("A"))
    return total_power


def tile_range(n: int) -> list[int]:
    return [x for x in (n // 6 - 1, n // 6) if x >= 0 and 6 * x <= n <= 6 * x + 7]


def subtiles(
    g: list[list[str]], i: int, j: int
) -> Iterator[tuple[int, int, list[list[str]]]]:
    """Gets the tile(s) including grid[i][j]"""

    for ii, jj in product(tile_range(i), tile_range(j)):
        if ii * 6 + 7 >= len(grid) or jj * 6 + 7 >= len(g[0]):
            continue
        tile = [g[i][jj * 6 : jj * 6 + 8] for i in range(ii * 6, ii * 6 + 8)]
        assert len(tile) == 8 and len(tile[0]) == 8
        yield ii, jj, tile


def horizontal_slice(desired: tuple[int]) -> Callable:
    def inner(
        tile: list[list[str]], i: int, j: int, unknowns: bool = False
    ) -> set[str]:
        assert 0 <= i < 8
        assert 0 <= j < 8
        assert len(tile) == 8 and len(tile[0]) == 8
        result = {tile[x][j] for x in desired}
        if not unknowns:
            result.discard(".")
            result.discard("?")
        return result

    return inner


def vertical_slice(desired: tuple[int]) -> Callable:
    def inner(
        tile: list[list[str]], i: int, j: int, unknowns: bool = False
    ) -> Callable:
        assert 0 <= i < 8
        assert 0 <= j < 8
        assert len(tile) == 8 and len(tile[0]) == 8

        result = {tile[i][x] for x in desired}
        if not unknowns:
            result.discard(".")
            result.discard("?")
        return result

    return inner


def solve_dot(g: list[list[str]], i: int, j: int) -> str:
    for ii, jj, tile in subtiles(g, i, j):
        offset_i = i - ii * 6
        offset_j = j - jj * 6
        h = horizontal_letters(tile, offset_i, offset_j)
        v = vertical_letters(tile, offset_i, offset_j)
        if solution := h & v:
            return solution.pop()
        if len(h) == 4:
            hs = horizontal_solution(tile, offset_i, offset_j)
            if len(hs) == 3:
                solution = h - hs
                return solution.pop()
        if len(v) == 4:
            vs = vertical_solution(tile, offset_i, offset_j)
            if len(vs) == 3:
                solution = v - vs
                return solution.pop()
    return None


def solve_question_mark(g: list[list[str]], i: int, j: int) -> str:
    for ii, jj, tile in subtiles(g, i, j):
        assert len(tile) == 8 and len(tile[0]) == 8
        offset_i = i - ii * 6
        offset_j = j - jj * 6
        hs = horizontal_solution(tile, offset_i, offset_j)
        hl = horizontal_letters(tile, offset_i, offset_j)
        if len(hs) == 4 and len(hl) == 3:
            solution = hs - hl
            return solution.pop()
        vs = vertical_solution(tile, offset_i, offset_j)
        vl = vertical_letters(tile, offset_i, offset_j)
        if len(vs) == 4 and len(vl) == 3:
            solution = vs - vl
            return solution.pop()
    return None


horizontal_letters = horizontal_slice((0, 1, 6, 7))
vertical_letters = vertical_slice((0, 1, 6, 7))

horizontal_solution = horizontal_slice((2, 3, 4, 5))
vertical_solution = vertical_slice((2, 3, 4, 5))

# Part 1:
grid = []

with open("everybody_codes_e2024_q10_p1.txt", "r") as file:
    for line in file:
        grid.append(list(line.strip()))

for i, j in product(range(len(grid)), range(len(grid[0]))):
    if grid[i][j] == "." and (solution := solve_dot(grid, i, j)):
        grid[i][j] = solution
p1_word = runic_word(grid)
print(f"Part 1: The runic word is {p1_word}")

# Part 2:
grids = []
total_power = 0

with open("everybody_codes_e2024_q10_p2.txt", "r") as file:
    this_row = []
    for line in file:
        if line.strip() == "":
            continue
        pieces = line.strip().split(" ")
        if len(this_row) < len(pieces):
            this_row.extend([[] for _ in range(len(pieces))])
        for j, piece in enumerate(pieces):
            this_row[j].append(list(piece))
        if len(this_row[0]) == 8:
            grids.extend(this_row)
            this_row = []

for g in grids:
    for i, j in product(range(len(grid)), range(len(grid[0]))):
        if g[i][j] == "." and (solution := solve_dot(g, i, j)):
            g[i][j] = solution
    total_power += word_power(runic_word(g))


print(f"Part 2: The total power is {total_power}")

# Part 3
grid = []
total_power = 0

with open("everybody_codes_e2024_q10_p3.txt", "r") as file:
    for line in file:
        grid.append(list(line.strip()))

previous_unknowns = None
current_unknowns = sum(g.count(".") + g.count("?") for g in grid)

while previous_unknowns != current_unknowns:
    for i, j in product(range(len(grid)), range(len(grid[0]))):
        if grid[i][j] == ".":
            if solution := solve_dot(grid, i, j):
                grid[i][j] = solution
        elif grid[i][j] == "?":
            if solution := solve_question_mark(grid, i, j):
                grid[i][j] = solution
    previous_unknowns = current_unknowns
    current_unknowns = sum(g.count(".") + g.count("?") for g in grid)

# Now compute the total
total_power = 0
# arbitrarily use offset 3,3 in each tile
for i in range(3, len(grid), 6):
    for j in range(3, len(grid[0]), 6):
        for _, _, tile in subtiles(grid, i, j):
            unknowns = sum(t.count(".") + t.count("?") for t in tile)
            if unknowns == 0:
                total_power += word_power(runic_word(tile))
print(f"Part 3: The total power is {total_power}")

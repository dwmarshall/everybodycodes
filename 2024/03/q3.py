directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
diagonal_directions = [
    (i, j) for i in range(-1, 2) for j in range(-1, 2) if (i, j) != (0, 0)
]


def total_blocks(g: set[tuple[int, int]], d: list[tuple[int, int]]) -> int:
    blocks = 0
    while g:
        blocks += len(g)
        new_g = set()
        for x, y in g:
            if all((x + dx, y + dy) in g for dx, dy in d):
                new_g.add((x, y))
        g = new_g
    return blocks


directions_list = [None, directions, directions, diagonal_directions]

for p in range(1, 4):
    with open(f"everybody_codes_e2024_q03_p{p}.txt", "r") as file:
        locations = set()
        for i, line in enumerate(file):
            for j, c in enumerate(line):
                if c == "#":
                    locations.add((i, j))
    blocks = total_blocks(locations, directions_list[p])
    print(f"Part {p}: There are {blocks} locations.")

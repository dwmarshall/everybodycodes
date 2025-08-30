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


def solve(
    g: tuple[tuple[str]], h: dict[tuple[int, int], str], origin: tuple[int, int]
) -> int:
    initial_state = (
        origin,  # position
        frozenset(),  # herbs acquired
    )
    states = {initial_state}
    visited = set()
    steps = 0
    while True:
        print(f"At step {steps}, there are {len(states)} states.")
        new_states = set()
        for current_state in states:
            if current_state in visited:
                continue
            visited.add(current_state)
            (x, y), herbs_acquired = current_state
            if (x, y) == origin and herbs_acquired == frozenset(h.values()):
                return steps
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if 0 <= ny < len(g) and 0 <= nx < len(g[0]) and g[ny][nx] not in "#~":
                    new_herbs_acquired = herbs_acquired
                    if (nx, ny) in h:
                        new_herbs_acquired = herbs_acquired | {h[(nx, ny)]}
                    new_state = ((nx, ny), frozenset(new_herbs_acquired))
                    new_states.add(new_state)
        states = new_states
        steps += 1


for p in range(1, 4):
    maze, start, herbs = input(p)
    print(f"Part {p}: minimum steps are {solve(maze, herbs, start)}")

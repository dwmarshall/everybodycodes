from collections import deque


def input(n: int, testing: bool = False) -> tuple[list[str], list[str]]:

    names: list[str]
    directions: list[str]
    filename = f"test{n}.txt" if testing else f"everybody_codes_e2025_q01_p{n}.txt"
    with open(filename, "r") as file:
        names = file.readline().rstrip().split(",")
        next(file)
        directions = file.readline().rstrip().split(",")
    return names, directions


# Part 1

names, directions = input(1)
index = 0
for instruction in directions:
    if instruction[0] == "L":
        index = max(0, index - int(instruction[1:]))
    else:
        index = min(len(names) - 1, index + int(instruction[1:]))
print(f"Part 1: Name is {names[index]}")

# Part 2

parents, family_tree = input(2)

dragons = deque(parents)

for instruction in family_tree:
    if instruction[0] == "L":
        dragons.rotate(int(instruction[1:]))
    else:
        dragons.rotate(-int(instruction[1:]))

print(f"Part 2: First parent is {dragons[0]}")

# Part 3

parents, family_tree = input(3)

for instruction in family_tree:
    index = int(instruction[1:]) % len(parents)
    if instruction[0] == "L":
        index = -index
    parents[0], parents[index] = parents[index], parents[0]

print(f"Part 3: Second parent is {parents[0]}")

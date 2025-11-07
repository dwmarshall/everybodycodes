def input(n: int, testing: bool = False) -> list[str]:
    filename = f"test{n}.txt" if testing else f"everybody_codes_e2025_q04_p{n}.txt"
    with open(filename, "r") as file:
        return file.readlines()


# Part 1
p1_lines = list(map(int, input(1)))

print(f"Part 1: {p1_lines[0] * 2025 // p1_lines[-1]}")

# Part 2
p2_lines = list(map(int, input(2)))

print(f"Part 2: {(10000000000000 * p2_lines[-1] + p2_lines[0] - 1) // p2_lines[0]}")

# Part 3
p3_lines = input(3)

gear_ratio = 1
for line in p3_lines[1:-1]:
    lower, higher = line.split("|")
    gear_ratio *= int(higher) // int(lower)

print(f"Part 3: {100 * int(p3_lines[0]) * gear_ratio // int(p3_lines[-1])}")

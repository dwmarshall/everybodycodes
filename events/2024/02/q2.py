def part1(s: list[str]) -> int:
    score = 0
    for line in s:
        if line.startswith("WORDS:"):
            words = line[6:].strip().split(",")
        else:
            for w in words:
                score += line.count(w)
    return score


def part2(s: list[str]) -> int:
    score = 0
    for line in s:
        if line.startswith("WORDS"):
            words = line[6:].strip().split(",")
            words += [w[::-1] for w in words]
        else:
            runes = [0] * len(line.strip())
            for i in range(len(line.strip())):
                for w in words:
                    if line[i:].startswith(w):
                        runes[i : i + len(w)] = [1] * len(w)
            score += sum(runes)
    return score


def part3(s: list[str]) -> int:
    grid = []
    runes = []
    for line in s:
        if line.startswith("WORDS:"):
            words = line[6:].strip().split(",")
        elif len(line.strip()) >= 1:
            grid.append(list(line.strip()))
            runes.append([0] * len(line.strip()))
    for w in words:
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                # check left to right
                if all(grid[x][(y + i) % len(grid[x])] == c for i, c in enumerate(w)):
                    for i in range(len(w)):
                        runes[x][(y + i) % len(grid[x])] = 1
                # check right to left
                if all(grid[x][(y - i) % len(grid[x])] == c for i, c in enumerate(w)):
                    for i in range(len(w)):
                        runes[x][(y - i) % len(grid[x])] = 1
                # check top to bottom
                if all(
                    x + i < len(grid) and grid[x + i][y] == c for i, c in enumerate(w)
                ):
                    for i in range(len(w)):
                        runes[x + i][y] = 1
                # check bottom to top
                if all(x - i >= 0 and grid[x - i][y] == c for i, c in enumerate(w)):
                    for i in range(len(w)):
                        runes[x - i][y] = 1
    return sum(sum(row) for row in runes)


parts = [None, part1, part2, part3]
for i in range(1, len(parts)):
    filename = f"everybody_codes_e2024_q02_p{i}.txt"
    with open(filename, "r") as file:
        print(f"Part {i}: Score is {parts[i](file.readlines())}")

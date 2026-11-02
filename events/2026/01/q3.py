import sys

needed: int = 0
frames: list[int] = [8]

with open(sys.argv[1], "r") as file:
    for line in file:
        numbers = list(map(int, line.split(",")))
        for c in numbers:
            while frames[-1] < c:
                new_side = 3 + len(frames) * 2
                frames.append(new_side * new_side - 1)
            for f in frames:
                if f >= c:
                    needed += f - c
                    break


print(needed)

from collections import Counter


def input(n: int, testing: bool = False) -> list[int]:

    filename = f"test{n}.txt" if testing else f"everybody_codes_e2025_q03_p{n}.txt"
    with open(filename, "r") as file:
        return list(map(int, file.readline().split(",")))


# Part 1

p1_boxes = Counter(input(1))
print(f"Part 1: Sum is {sum(p1_boxes.keys())}")

# Part 2

p2_boxes = Counter(input(2))
p2_sizes = sorted(p2_boxes.keys())
print(f"Part 2: Sum is {sum(p2_sizes[:20])}")

# Part 3
p3_boxes = Counter(input(3))
print(f"Part 3: Sets required are {p3_boxes.most_common(1)[0][1]}")

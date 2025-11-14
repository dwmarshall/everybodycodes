import re


class Complex:
    def __init__(self, X: int, Y: int):
        self.X = X
        self.Y = Y

    def __add__(self, other: "Complex") -> "Complex":
        return Complex(self.X + other.X, self.Y + other.Y)

    def __mul__(self, other: "Complex") -> "Complex":
        newX = self.X * other.X - self.Y * other.Y
        newY = self.X * other.Y + self.Y * other.X
        return Complex(newX, newY)

    def __truediv__(self, other: "Complex") -> "Complex":
        return Complex(int(self.X / other.X), int(self.Y / other.Y))

    def __str__(self):
        return f"[{self.X},{self.Y}]"


def input(n: int, testing: bool = False) -> tuple[int, int]:
    filename = f"test{n}.txt" if testing else f"everybody_codes_e2025_q02_p{n}.txt"
    with open(filename) as file:
        numbers = re.findall(r"-?\d+", file.read())
        return int(numbers[0]), int(numbers[1])


# Part 1
a = Complex(*input(1))
r = Complex(0, 0)

for _ in range(3):
    r *= r
    r /= Complex(10, 10)
    r += a
print(f"Part 1: {r}")

# Part 2
total_points = 0
D = Complex(100000, 100000)

a = Complex(*input(2))
for x in range(a.X, a.X + 1010, 10):
    for y in range(a.Y, a.Y + 1010, 10):
        total_points += 1
        p = Complex(x, y)
        r = Complex(0, 0)
        for i in range(100):
            r *= r
            r /= D
            r += p
            if abs(r.X) > 1_000_000 or abs(r.Y) > 1_000_000:
                total_points -= 1
                break
print(f"Part 2: Total points are {total_points}")

# Part 3
total_points = 0

a = Complex(*input(3))
for x in range(a.X, a.X + 1001):
    for y in range(a.Y, a.Y + 1001):
        total_points += 1
        p = Complex(x, y)
        r = Complex(0, 0)
        for i in range(100):
            r *= r
            r /= D
            r += p
            if abs(r.X) > 1_000_000 or abs(r.Y) > 1_000_000:
                total_points -= 1
                break
print(f"Part 2: Total points are {total_points}")

def input(n: int, testing: bool = False) -> list[dict[str, int]]:
    lines: list[dict[str, int]] = []

    filename = f"test{n}.txt" if testing else f"everybody_codes_e1_q01_p{n}.txt"
    with open(filename, "r") as file:
        for line in file:
            d = {k: int(v) for k, v in (pair.split("=") for pair in line.split())}
            lines.append(d)
    return lines


def eni(n: int, exp: int, mod: int) -> int:
    remainders: list[str] = []

    score: int = 1
    for _ in range(exp):
        score *= n
        score %= mod
        remainders.append(str(score))
    remainders.reverse()
    return int("".join(remainders))


highest_sum = 0

for note in input(1):
    note_sum = eni(note["A"], note["X"], note["M"])
    note_sum += eni(note["B"], note["Y"], note["M"])
    note_sum += eni(note["C"], note["Z"], note["M"])
    highest_sum = max(highest_sum, note_sum)

print(highest_sum)

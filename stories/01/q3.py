def input(n: int, testing: bool = False) -> list[dict[str, int]]:
    lines: list[dict[str, int]] = []

    filename = f"test{n}.txt" if testing else f"everybody_codes_e1_q01_p{n}.txt"
    with open(filename, "r") as file:
        for line in file:
            d = {k: int(v) for k, v in (pair.split("=") for pair in line.split())}
            lines.append(d)
    return lines


def eni_cycle(n: int, _: int, mod: int) -> tuple[list[int], list[int]]:
    remainders: list[int] = []

    score = 1
    while True:
        score *= n
        score %= mod
        if score == 0:
            return remainders, [0]
        elif score in remainders:
            cutoff = remainders.index(score)
            return remainders[:cutoff], remainders[cutoff:]
        remainders.append(score)


def eni_sum(n: int, exp: int, mod: int) -> int:
    prefix, cycle = eni_cycle(n, exp, mod)

    if exp <= len(prefix):
        return sum(prefix[:exp])

    running_sum = sum(prefix)
    exp -= len(prefix)

    cycles, remainder = divmod(exp, len(cycle))
    running_sum += cycles * sum(cycle)
    running_sum += sum(cycle[:remainder])
    return running_sum


highest_sum = 0

for note in input(3):
    note_sum = eni_sum(note["A"], note["X"], note["M"])
    note_sum += eni_sum(note["B"], note["Y"], note["M"])
    note_sum += eni_sum(note["C"], note["Z"], note["M"])
    highest_sum = max(highest_sum, note_sum)

print(highest_sum)

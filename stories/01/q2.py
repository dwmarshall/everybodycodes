REMAINDERS = 5


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


def eni(n: int, exp: int, mod: int) -> int:
    # print(f"Calculating eni({n}, {exp}, {mod})")
    prefix, cycle = eni_cycle(n, exp, mod)

    remainders: list[int]

    length = exp - len(prefix)
    if length < 0:
        remainders = prefix[:exp]
        # print(f"n={n}, exp={exp}, mod={mod} => {remainders}")
    elif exp < len(cycle):
        remainders = cycle[:exp]
        # print(f"n={n}, exp={exp}, mod={mod} => {remainders}")
    else:
        remainders = []
        while len(remainders) < REMAINDERS:
            remainders.extend(cycle)
        length_mod = length % len(cycle)
        remainders.extend(cycle[:length_mod])
    result = int("".join(str(r) for r in reversed(remainders[-REMAINDERS:])))
    # print(f"n={n}, exp={exp}, mod={mod} => {result}")
    return result


highest_sum = 0

for note in input(2):
    note_sum = eni(note["A"], note["X"], note["M"])
    note_sum += eni(note["B"], note["Y"], note["M"])
    note_sum += eni(note["C"], note["Z"], note["M"])
    highest_sum = max(highest_sum, note_sum)

print(highest_sum)

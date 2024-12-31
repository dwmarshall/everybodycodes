from collections.abc import Callable
from itertools import product

monsters = {"A": 0, "B": 1, "C": 3, "D": 5}

double_monsters = {}

for t in product("xABCD", "xABCD"):
    combo = 2 if all(x in monsters for x in t) else 0
    for m in t:
        if m in monsters:
            combo += monsters[m]
    double_monsters["".join(t)] = combo

triple_monsters = {}

for t in product("xABCD", "xABCD", "xABCD"):
    num_monsters = sum(1 if m in monsters else 0 for m in t)
    combo = 6 if num_monsters == 3 else 2 if num_monsters == 2 else 0
    for m in t:
        if m in monsters:
            combo += monsters[m]
    triple_monsters["".join(t)] = combo


def generator(table: dict[str, int], n: int) -> Callable:
    def part(s: str) -> int:
        return sum(table[s[i : i + n]] for i in range(0, len(s), n))

    return part


parts = [
    None,
    generator(monsters, 1),
    generator(double_monsters, 2),
    generator(triple_monsters, 3),
]

for i in range(1, 4):
    filename = f"everybody_codes_e2024_q01_p{i}.txt"
    with open(filename, "r") as file:
        print(f"Part {i}: {parts[i](file.readline().strip())} potions needed.")

from collections import Counter
import copy
from functools import cache, cached_property
from math import lcm


class Machine:

    def __init__(self, turns: tuple[int], reels: tuple[tuple[str]]):
        self.turns = turns
        self.reels = reels
        self.state = (0,) * len(turns)

    def __eq__(self, other):
        return (
            isinstance(other, Machine)
            and self.turns == other.turns
            and self.reels == other.reels
            and self.state == other.state
        )

    def __hash__(self):
        return hash((self.turns, self.reels, self.state))

    @cached_property
    def period(self) -> int:
        return lcm(*[len(x) for x in self.reels])

    def output(self) -> str:
        pieces = []
        for i in range(len(self.state)):
            pieces.append(self.reels[i][self.state[i]])
        return " ".join(pieces)

    def spin(self) -> None:
        new_state = list(self.state)
        for i in range(len(self.state)):
            new_state[i] = (self.state[i] + self.turns[i]) % len(self.reels[i])
        self.state = tuple(new_state)

    def bump(self, n: int) -> None:
        new_state = list(self.state)
        for i in range(len(self.state)):
            new_state[i] = (self.state[i] + n) % len(self.reels[i])
        self.state = new_state

    def coins(self) -> int:
        c = Counter()
        for i in range(len(self.state)):
            symbol = self.reels[i][self.state[i]]
            assert len(symbol) == 3
            c[symbol[0]] += 1
            c[symbol[2]] += 1
        win = 0
        for matching_symbols in c.values():
            if matching_symbols >= 3:
                win += matching_symbols - 2
        return win


def input(n: int, testing: bool = False) -> list[str]:
    filename = "test.txt" if testing else f"everybody_codes_e2024_q16_p{n}.txt"
    with open(filename, "r") as file:
        turns = tuple(map(int, file.readline().split(",")))
        reels = [[] for _ in range(len(turns))]
        # Discard an empty line
        assert file.readline() == "\n"
        for line in file:
            for i in range(len(reels)):
                if (
                    4 * i + 3 <= len(line)
                    and (symbol := line[4 * i : 4 * i + 3]) != "   "
                ):
                    reels[i].append(symbol)
        for i in range(len(reels)):
            reels[i] = tuple(reels[i])
    return Machine(turns, tuple(reels))


@cache
def analyze(machine: Machine, spins: int) -> tuple[int, int]:
    if spins == 0:
        return 0, 0
    results = []
    machine = copy.deepcopy(machine)
    bumped_up = copy.deepcopy(machine)
    bumped_up.bump(1)
    bumped_down = copy.deepcopy(machine)
    bumped_down.bump(-1)

    for m in [machine, bumped_up, bumped_down]:
        m.spin()
        m_coins = m.coins()
        m_most, m_least = analyze(m, spins - 1)
        results.append(m_coins + m_most)
        results.append(m_coins + m_least)

    return max(results), min(results)


# Part 1

machine = input(1)
for _ in range(100):
    machine.spin()
print(f"Part 1: The output after 100 spins is {machine.output()}")

# Part 2

SPINS = 202420242024

machine = input(2)
total_coins = 0

coins = []
for _ in range(machine.period):
    machine.spin()
    coins.append(machine.coins())


number_of_cycles, remainder = divmod(SPINS, machine.period)

print(
    f"Part 2: The total winnings are {number_of_cycles * sum(coins) + sum(coins[:remainder])}"
)

# Part 3

machine = input(3)
most, least = analyze(machine, 256)
print(f"Part 3: The maximum and minimum are {most} {least}")

print(analyze.cache_info())

from collections.abc import Callable
from functools import cache


def input(n: int, testing: bool = False) -> dict[str, list[str]]:
    growth_table = dict()
    filename = "test.txt" if testing else f"everybody_codes_e2024_q11_p{n}.txt"
    with open(filename, "r") as file:
        for line in file:
            termite, spawn = line.strip().split(":")
            growth_table[termite] = tuple(spawn.split(","))

    return growth_table


def population_counter(table: dict[str, list[str]]) -> Callable:
    @cache
    def population(termite: str, days: int) -> int:
        if days == 0:
            return 1
        termite_counter = 0
        for t in table[termite]:
            termite_counter += population(t, days - 1)
        return termite_counter

    return population


def population_generator(table: dict[str, list[str]]) -> Callable:
    @cache
    def population(termites: tuple[str], days: int) -> tuple[str]:
        if days == 0:
            return termites
        result = tuple()
        if days % 2 == 0:
            for t in termites:
                halfway = population((t,), days // 2)
                for t2 in halfway:
                    result += population((t2,), days // 2)
        else:
            for t in termites:
                for x in table[t]:
                    result += population((x,), days - 1)

        return result

    return population


# def population_generator(table: dict[str, list[str]]) -> Callable:
#     @cache
#     def population(termites: tuple[str], days: int) -> tuple[str]:
#         if days == 0:
#             return termites
#         result = tuple()
#         for t in termites:
#             for x in table[t]:
#                 result += population((x,), days - 1)
#         return result

#     return population


starting_termite = [None, "A", "Z"]
days = [None, 4, 10]

for p in range(1, 3):
    pop_counter = population_counter(input(p))
    print(
        f"Part {p}: After {days[p]} days there are {pop_counter(starting_termite[p], days[p])} termites."
    )

# Part 3
P3_DAYS = 20
growth_table = input(3)
p3_counter = population_counter(growth_table)


populations = [p3_counter(x, P3_DAYS) for x in growth_table]
print(
    f"Part 3: The maximum difference after {P3_DAYS} days is {max(populations) - min(populations)}"
)

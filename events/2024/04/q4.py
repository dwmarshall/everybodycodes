from statistics import median


def hits(nails: list[int], desired_height: int) -> int:
    return sum(abs(n - desired_height) for n in nails)


for p in range(1, 4):
    with open(f"everybody_codes_e2024_q04_p{p}.txt", "r") as file:
        heights = list(map(int, file.readlines()))
        d = int(median(heights)) if p == 3 else min(heights)
        print(f"Part {p}: {hits(heights, d)}")

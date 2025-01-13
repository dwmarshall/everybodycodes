from functools import cache

CATAPULTS = {(0, 0): 1, (0, 1): 2, (0, 2): 3}


@cache
def shot_path(catapult: tuple[int, int], power: int) -> dict[tuple[int, int], int]:
    path_dict = dict()
    x, y = catapult
    x, y = x + power, y + power
    t = power
    for _ in range(power):
        path_dict[(x, y)] = t
        x += 1
        t += 1
    while y >= 0:
        path_dict[(x, y)] = t
        x, y = x + 1, y - 1
        t += 1
    return path_dict


def meteor_path(meteor: tuple[int, int]) -> tuple[tuple[tuple[int, int], int]]:
    path = []
    x, y = meteor
    t = x // 2
    x, y = x - t, y - t
    while y >= 0:
        path.append(((x, y), t))
        x, y = x - 1, y - 1
        t += 1
    return path


def ranking(meteor: tuple[int, int]) -> int:
    """The best shot we can get at some meteor"""
    for m_position, m_time in meteor_path(meteor):
        mx, my = m_position
        hits = []
        for (cx, cy), c_factor in CATAPULTS.items():
            max_power = max(mx, my) - cy
            for power in range(max_power, 0, -1):
                shot_points = shot_path((cx, cy), power)
                if m_position in shot_points and shot_points[m_position] <= m_time:
                    hits.append(power * c_factor)
        if hits:
            return min(hits)


meteors = []

with open("everybody_codes_e2024_q12_p3.txt", "r") as file:
    for line in file:
        meteors.append(tuple(map(int, line.split())))


total_ranking = 0

for i, m in enumerate(meteors):
    this_ranking = ranking(m)
    assert this_ranking is not None
    print(f"Ranking for {m} (# {i}) is {this_ranking}")
    total_ranking += this_ranking

print(f"Part 3: Combined ranking is {total_ranking}")

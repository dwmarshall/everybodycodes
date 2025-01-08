import math

P1_STAMPS = [1, 3, 5, 10]
P2_STAMPS = [1, 3, 5, 10, 15, 16, 20, 24, 25, 30]
P3_STAMPS = [1, 3, 5, 10, 15, 16, 20, 24, 25, 30, 37, 38, 49, 50, 74, 75, 100, 101]


ALL_STAMPS = [None, P1_STAMPS, P2_STAMPS, P3_STAMPS]


def unistamps_needed(balls: list[int], stamps: list[int]) -> int:
    max_ball = max(balls)
    dp = [math.inf] * (max_ball + 1)
    dp[0] = 0

    for i in range(max_ball + 1):
        for s in stamps:
            if i + s <= max_ball:
                dp[i + s] = min(dp[i + s], dp[i] + 1)
    return sum(dp[x] for x in balls)


def doublestamps_needed(balls: list[int], stamps: list[int]) -> int:
    max_ball = max(balls)
    max_needed = (max_ball - 100) // 2 + 100
    dp = [math.inf] * (max_needed + 1)
    dp[0] = 0

    for i in range(max_needed + 1):
        for s in stamps:
            if i + s <= max_needed:
                dp[i + s] = min(dp[i + s], 1 + dp[i])

    total_needed = 0
    for b in balls:
        stamps_needed = math.inf
        for i in range(max_needed + 1):
            if b - i <= max_needed and abs(b - 2 * i) <= 100:
                stamps_needed = min(stamps_needed, dp[i] + dp[b - i])
        total_needed += stamps_needed
    return total_needed


parts = [None, unistamps_needed, unistamps_needed, doublestamps_needed]

for p in range(1, 4):
    grand_total = 0
    sparkballs = []
    with open(f"everybody_codes_e2024_q09_p{p}.txt", "r") as file:
        for line in file:
            sparkballs.append(int(line))

    print(f"Part {p}: {parts[p](sparkballs, ALL_STAMPS[p])} stamps are needed.")

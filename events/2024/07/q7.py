from collections import Counter
from collections.abc import Iterator
from itertools import cycle, islice

TEST_TRACK = """
S+===
-   +
=+=-+
""".strip()

P2_TRACK = """
S-=++=-==++=++=-=+=-=+=+=--=-=++=-==++=-+=-=+=-=+=+=++=-+==++=++=-=-=--
-                                                                     -
=                                                                     =
+                                                                     +
=                                                                     +
+                                                                     =
=                                                                     =
-                                                                     -
--==++++==+=+++-=+=-=+=-+-=+-=+-=+=-=+=--=+++=++=+++==++==--=+=++==+++-
""".strip()

P3_TRACK = """
S+= +=-== +=++=     =+=+=--=    =-= ++=     +=-  =+=++=-+==+ =++=-=-=--
- + +   + =   =     =      =   == = - -     - =  =         =-=        -
= + + +-- =-= ==-==-= --++ +  == == = +     - =  =    ==++=    =++=-=++
+ + + =     +         =  + + == == ++ =     = =  ==   =   = =++=
= = + + +== +==     =++ == =+=  =  +  +==-=++ =   =++ --= + =
+ ==- = + =   = =+= =   =       ++--          +     =   = = =--= ==++==
=     ==- ==+-- = = = ++= +=--      ==+ ==--= +--+=-= ==- ==   =+=    =
-               = = = =   +  +  ==+ = = +   =        ++    =          -
-               = + + =   +  -  = + = = +   =        +     =          -
--==++++==+=+++-= =-= =-+-=  =+-= =-= =--   +=++=+++==     -=+=++==+++-
""".strip()

STEPS = {"+": 1, "=": 0, "-": -1}

STARTING_ESSENCE = 10

directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def all_plans(pluses: int = 5, minuses: int = 3, equals: int = 3) -> Iterator[str]:
    if pluses == 0 and minuses == 0 and equals == 0:
        yield ""
    if pluses > 0:
        for subplan in all_plans(pluses - 1, minuses, equals):
            yield "+" + subplan
    if minuses > 0:
        for subplan in all_plans(pluses, minuses - 1, equals):
            yield "-" + subplan
    if equals > 0:
        for subplan in all_plans(pluses, minuses, equals - 1):
            yield "=" + subplan


def parse_track(track: str) -> list[str]:
    grid = [list(x.strip()) for x in track.split("\n")]

    output = []
    dir = 0
    x, y = 1, 0

    while grid[y][x] != "S":
        output.append(grid[y][x])
        dx, dy = directions[dir]
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[ny]) and grid[ny][nx] != " ":
            x, y = nx, ny
        else:
            turn_right = (dir + 1) % 4
            dx, dy = directions[turn_right]
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[ny]) and grid[ny][nx] != " ":
                dir = turn_right
                x, y = nx, ny
            else:
                dir = (dir - 1) % 4
                dx, dy = directions[dir]
                x, y = x + dx, y + dy
    output.append("=")  # we didn't record the finishing S
    return "".join(output)


def parse_input(part: int) -> dict:
    plans = dict()

    with open(f"everybody_codes_e2024_q07_p{part}.txt", "r") as file:
        for line in file:
            id, s = line.strip().split(":")
            plans[id] = list(s.split(","))

    return plans


def execute_plan(track: str, plan: str, rounds: int) -> int:
    essence = STARTING_ESSENCE
    total_essence = 0

    for track_segment, plan_segment in zip(track * rounds, cycle(plan)):
        match (track_segment, plan_segment):
            case ("=", x):
                essence += STEPS[x]
            case ("+", _):
                essence += 1
            case ("-", _):
                essence -= 1
        total_essence += essence

    return total_essence


# Part 1

p1_plans = parse_input(1)
p1_essence = dict()
for p in p1_plans:
    total_essence = 0
    plan_essence = STARTING_ESSENCE
    for delta in islice(cycle(p1_plans[p]), 10):
        plan_essence += STEPS[delta]
        total_essence += plan_essence
    p1_essence[p] = total_essence

ids = list(p1_plans.keys())
ids.sort(key=lambda x: p1_essence[x], reverse=True)
print(f"Part 1: Final ranking is {"".join(ids)}")

# Part 2

p2_track = parse_track(P2_TRACK)

p2_plans = parse_input(2)

essence = Counter({p: STARTING_ESSENCE for p in p2_plans})
total_essence = Counter()

for id, plan in p2_plans.items():
    total_essence[id] = execute_plan(p2_track, plan, 10)

print(
    f"Part 2: Finishing order is {"".join(t[0] for t in total_essence.most_common())}"
)

# Part 3

p3_track = parse_track(P3_TRACK)

p3_plans = parse_input(3)
opponent_essence = execute_plan(p3_track, p3_plans["A"], 11)

num_winning_plans = 0

for plan in all_plans():
    essence = execute_plan(p3_track, plan, 11)
    if essence > opponent_essence:
        num_winning_plans += 1

print(f"Part 3: There are {num_winning_plans} winning plans.")

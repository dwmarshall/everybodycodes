from collections import defaultdict, deque


def input(n: int, testing: bool = False) -> tuple[list[str], list[str]]:
    filename = f"test{n}.txt" if testing else f"everybody_codes_e2025_q07_p{n}.txt"
    with open(filename) as file:
        names = file.readline().strip().split(",")
        file.readline()
        rules: list[str] = []
        for line in file:
            rules.append(line.strip())
        return names, rules


def parsed_rules(rules: list[str]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = defaultdict(list[str])
    for rule in rules:
        left, right = rule.split(" > ")
        result[left].extend(right.split(","))
    return result


MIN_LENGTH = 7
MAX_LENGTH = 11


def suffixes(prefix: str, ruleset: dict[str, list[str]]) -> list[str]:
    output: list[str] = []
    work_queue = deque([prefix])
    # Is our prefix valid?
    valid = True
    for i in range(len(prefix) - 1):
        if prefix[i + 1] not in ruleset[prefix[i]]:
            valid = False
            break
    if valid:
        while work_queue:
            work_name = work_queue.popleft()
            for next_char in ruleset[work_name[-1]]:
                new_name = work_name + next_char
                if len(new_name) >= MIN_LENGTH:
                    output.append(new_name)
                if len(new_name) < MAX_LENGTH:
                    work_queue.append(new_name)
    return output


# Part 1

names, rules = input(1)
parsed = parsed_rules(rules)

for name in names:
    success = True
    for i in range(len(name) - 1):
        if name[i + 1] not in parsed[name[i]]:
            success = False
            break
    if success:
        print(f"Part 1: {name} is the winner")

# Part 2
names, rules = input(2)
parsed = parsed_rules(rules)

index_sum = 0

for index, name in enumerate(names):
    success = True
    for i in range(len(name) - 1):
        if name[i + 1] not in parsed[name[i]]:
            success = False
            break
    if success:
        index_sum += index + 1

print(f"Part 2: Sum of indices is {index_sum}")

# Part 3
names, rules = input(3)
parsed = parsed_rules(rules)
all_names: set[str] = set()

for n in names:
    all_names.update(suffixes(n, parsed))

print(f"Part 3: There are {len(all_names)} possible names")

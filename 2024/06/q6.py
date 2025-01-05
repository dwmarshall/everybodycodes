from collections import defaultdict


def unique_path(g: dict[str, list]) -> list[str]:
    paths = [["RR"]]
    while paths:
        new_paths = []
        for p in paths:
            curr = p[-1]
            for n in graph[curr]:
                new_paths.append(p + [n])
        fruit_count = sum(1 if np[-1] == "@" else 0 for np in new_paths)
        if fruit_count == 1:
            for np in new_paths:
                if np[-1] == "@":
                    return np
        paths = new_paths


def paths(g: dict[str, list]) -> list[list[str]]:
    paths = [["RR"]]
    found_paths = []
    while paths:
        new_paths = []
        for p in paths:
            curr = p[-1]
            if curr == "@":
                found_paths.append(p)
                continue
            for n in graph[curr]:
                new_paths.append(p + [n])
        paths = new_paths
    return found_paths


def part1(g: dict[str, list]) -> str:
    return "".join(unique_path(g))


def partN(g: dict[str, list]) -> str:
    return "".join(x[0] for x in unique_path(g))


parts = [None, part1, partN, partN]

for p in range(1, 4):
    graph = defaultdict(list)
    with open(f"everybody_codes_e2024_q06_p{p}.txt", "r") as file:
        for line in file:
            node, others = line.strip().split(":")
            graph[node].extend(others.split(","))

    print(f"Part {p}: Best path is {parts[p](graph)}")

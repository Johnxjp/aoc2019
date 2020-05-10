from collections import defaultdict
from typing import Mapping, Sequence, Tuple
from helper import loadv4


def parse_line(orbits: str) -> Tuple[str, str]:
    """Returns a tuple of strings. The first is the planet being orbitted and
    the second is the satellite"""
    return orbits.strip().split(")")


def parse(data: Sequence[str]) -> Mapping[str, Sequence[str]]:
    core_to_satellites_map = defaultdict(list)
    for line in data:
        core, satellite = parse_line(line)
        core_to_satellites_map[core].append(satellite)

    return core_to_satellites_map


def total_orbits(
    satellite_map: Mapping[str, Sequence[str]], current_core="COM", depth=1
) -> int:
    if current_core not in satellite_map:
        return 0

    total = 0
    for child in satellite_map[current_core]:
        total += total_orbits(satellite_map, child, depth + 1) + depth

    return total


def main():
    data = loadv4("data/d6.txt")
    data = parse(data)
    # Compute total orbits
    return total_orbits(data)


if __name__ == "__main__":
    print(main())

    # map = {
    #     "COM": ["B"],
    #     "B": ["G", "C"],
    #     "G": ["H"],
    #     "C": ["D"],
    #     "D": ["E", "I"],
    #     "E": ["F", "J"],
    #     "J": ["K"],
    #     "K": ["L"],
    # }
    # print(total_orbits(map))

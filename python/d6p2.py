from dataclasses import dataclass
from collections import defaultdict
from typing import Mapping, Optional, Sequence, Tuple
from helper import loadv4


def parse_line(orbits: str) -> Tuple[str, str]:
    """
    Returns a tuple of strings. The first is the planet being orbitted and
    the second is the satellite
    """
    return orbits.strip().split(")")


def parse(data: Sequence[str]) -> Mapping[str, Sequence[str]]:
    core_to_satellites_map = defaultdict(list)
    satellite_to_core_map = defaultdict(list)
    for line in data:
        core, satellite = parse_line(line)
        core_to_satellites_map[core].append(satellite)
        satellite_to_core_map[satellite].append(core)

    return core_to_satellites_map, satellite_to_core_map


def find_distance(
    satellite_map: Mapping[str, Sequence[str]],
    core_map: Mapping[str, Sequence[str]],
    start="YOU",
    target="SAN",
) -> int:
    visited = set({start})
    to_visit = core_map[start] + satellite_map[start]
    n = 1
    while to_visit:
        next_places = []
        for obj in to_visit:
            visited.add(obj)
            for next_place in core_map[obj] + satellite_map[obj]:
                if next_place == target:
                    return n - 1

                if next_place not in visited:
                    next_places.append(next_place)

        to_visit = next_places
        n += 1

    return -1


def main():
    data = loadv4("data/d6.txt")
    c2s, s2c = parse(data)
    return find_distance(c2s, s2c)


if __name__ == "__main__":
    print(main())

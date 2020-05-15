from collections import defaultdict
from dataclasses import dataclass
from math import pi, atan2
from typing import Sequence, Tuple


@dataclass
class Point:
    x: int
    y: int


def load_asteroid_map(file: str) -> Sequence[Sequence[str]]:
    asteroid_map = []
    with open(file) as f:
        for line in f:
            asteroid_map.append(list(line.strip()))

    return asteroid_map


def calculate_angle(p1: Point, p2: Point) -> float:
    if p2.y == p1.y:
        return pi / 2 if p2.x > p1.x else -pi / 2
    if p2.x == p1.x:
        return 0 if p2.y > p1.y else pi

    return atan2(p2.y - p1.y, p2.x - p1.x)


def get_coords(map: Sequence[Sequence[str]]) -> Sequence[Point]:
    """Treat x as horizontal and y as vertical"""
    coords = []
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == "#":
                coords.append(Point(j, i))

    return coords


def asteroids_can_see(idx: int, asteroid_coords: Sequence[Point]) -> int:
    angles = defaultdict(list)
    for i, asteroid in enumerate(asteroid_coords):
        if i != idx:
            angle = calculate_angle(asteroid_coords[idx], asteroid_coords[i])
            angles[angle].append((asteroid_coords[idx], asteroid_coords[i]))

    return len(angles.keys())


def main():
    map = load_asteroid_map("data/d10.txt")
    asteroid_coords = get_coords(map)
    points = {}
    for idx in range(len(asteroid_coords)):
        points[(asteroid_coords[idx].x, asteroid_coords[idx].y)] = asteroids_can_see(
            idx, asteroid_coords
        )

    n_visible = 0
    laser_station = Point(-1, -1)
    for k, v in points.items():
        if v > n_visible:
            laser_station = k
            n_visible = v
    return laser_station, n_visible


if __name__ == "__main__":
    print(main())

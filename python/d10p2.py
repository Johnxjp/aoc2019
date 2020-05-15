from collections import defaultdict
from dataclasses import dataclass
from math import pi, atan2, sqrt
from typing import Sequence, Tuple


@dataclass
class Point:
    x: int
    y: int

    def __eq__(self, other: "Point") -> bool:
        return (self.x == other.x) and (self.y == other.y)

    @property
    def distance(self):
        """Euclidean distance from origin"""
        return sqrt((self.y) ** 2 + (self.x) ** 2)

    @property
    def angle(self):
        """Angle from origin. 0 degrees is UP and angle grows clockwise"""
        val = atan2(self.x, self.y)
        if val >= 0:
            return val
        else:
            return 2 * pi + val


def load_asteroid_map(file: str) -> Sequence[Sequence[str]]:
    asteroid_map = []
    with open(file) as f:
        for line in f:
            asteroid_map.append(list(line.strip()))

    return asteroid_map


def get_coords(map: Sequence[Sequence[str]]) -> Sequence[Point]:
    """Treat x as horizontal and y as vertical"""
    coords = []
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == "#":
                coords.append(Point(j, i))

    return coords


def calculate_distance(p1: Point, p2: Point) -> float:
    """Returns euclidean distance between points"""
    return sqrt((p2.y - p1.y) ** 2 + (p2.x - p1.x) ** 2)


def asteroid_destruction_order(coords: Sequence[Point]) -> Sequence[int]:
    """Computes the information (angles & distances) for each point relative to the origin"""
    n_asteroids = len(coords)
    angles_map = defaultdict(list)
    for point in coords:
        angles_map[point.angle].append(point)

    # Sort points by distance (descending)
    for angle in angles_map.keys():
        angles_map[angle] = sorted(
            angles_map[angle], key=lambda x: x.distance, reverse=True
        )

    destruction_order = []
    sorted_angles = sorted(angles_map.keys())
    # Keep rotating till all asteroids are destroyed
    while len(destruction_order) < n_asteroids:
        for angle in sorted_angles:
            if angles_map[angle]:
                destruction_order.append(angles_map[angle].pop())

    return destruction_order


def main():
    map = load_asteroid_map("data/d10.txt")
    asteroid_coords = get_coords(map)
    base_coord = Point(23, 19)  # From part 1

    # Flip the y so up is positive instead of down
    relative_coords = [
        Point(p.x - base_coord.x, -(p.y - base_coord.y)) for p in asteroid_coords
    ]
    # Remove the new origin
    point = relative_coords.pop(relative_coords.index(Point(0, 0)))
    destruction_order = asteroid_destruction_order(relative_coords)

    point_200 = destruction_order[199]
    # Shift back to normal coords
    point_200 = Point(base_coord.x + point_200.x, base_coord.y - point_200.y)
    return point_200.x * 100 + point_200.y


if __name__ == "__main__":
    print(main())

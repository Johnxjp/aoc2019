from typing import Sequence, Set, Tuple
from helper import loadv3


def parse_instruction(instruction: str) -> Tuple[str, int]:
    """
    Parses an instruction like R1 and returns the direction and distance
    """
    direction, distance = instruction[0], int(instruction[1:])
    return direction, distance


def generate_route(
    direction: str, distance: int, current_x: int = 0, current_y: int = 0
) -> Sequence[Tuple[int, int]]:

    if direction == "R":
        path = [(i, 0) for i in range(1, distance + 1)]
    elif direction == "L":
        path = [(-i, 0) for i in range(1, distance + 1)]
    elif direction == "U":
        path = [(0, i) for i in range(1, distance + 1)]
    else:
        path = [(0, -i) for i in range(1, distance + 1)]
    return [(current_x + x, current_y + y) for x, y in path]


def route(instructions: Sequence[str]) -> Set[Tuple[int, int]]:
    path = []
    for instruction in instructions:
        direction, distance = parse_instruction(instruction)
        if path:
            current_x, current_y = path[-1]
        else:
            current_x, current_y = 0, 0

        route = generate_route(direction, distance, current_x, current_y)
        path.extend(route)

    return set(path)


def manhattan_distance(x: int, y: int) -> int:
    return abs(x) + abs(y)


def intersection_points(
    path1: Set[Tuple[int, int]], path2: Set[Tuple[int, int]]
) -> Sequence[Tuple[int, int]]:
    return list(path1.intersection(path2))


def main():
    wire1_instructions, wire2_instructions = loadv3("data/d3.txt")
    path1 = route(wire1_instructions)
    path2 = route(wire2_instructions)
    points = intersection_points(path1, path2)  # 0, 0 is not included in these points
    distances = [manhattan_distance(x, y) for x, y in points]
    return min(distances)


if __name__ == "__main__":
    print(main())

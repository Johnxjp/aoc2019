from contextlib import suppress
from typing import Mapping, Sequence, Tuple
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


def route(instructions: Sequence[str]) -> Mapping[Tuple[int, int], int]:
    path = {}
    current_x, current_y, current_steps = 0, 0, 0
    for instruction in instructions:
        direction, distance = parse_instruction(instruction)
        route = generate_route(direction, distance, current_x, current_y)
        current_x, current_y = route[-1]
        for s, (x, y) in enumerate(route, 1):
            recorded_steps = path.get((x, y), 0)
            if recorded_steps:
                path[(x, y)] = min(s + current_steps, recorded_steps)
            else:
                path[(x, y)] = s + current_steps

        current_steps += len(route)

    return path


def main():
    wire1_instructions, wire2_instructions = loadv3("data/d3.txt")
    path1 = route(wire1_instructions)
    path2 = route(wire2_instructions)
    intersections = set(path1.keys())&set(path2.keys())
    return min(path1[p] + path2[p] for p in intersections)


if __name__ == "__main__":
    print(main())

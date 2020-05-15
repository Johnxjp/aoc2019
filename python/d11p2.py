from typing import Mapping, Tuple
from helper import loadv2
from intcode import Intcode


def update_direction(output: int, current_direction: str) -> str:
    directions = "URDL"
    index = directions.index(current_direction)
    increment = 1 if output else -1
    new_index = ((index + increment) + len(directions)) % len(directions)
    return directions[new_index]


def paint(computer: Intcode) -> Mapping[Tuple[int, int], int]:
    """O is black, 1 is white"""
    BLACK, current_pos, panel_colours = 0, (0, 0), {(0, 0): 1}
    direction_map = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}
    direction = "U"
    while True:
        current_panel_colour = panel_colours.get(current_pos, BLACK)
        colour = computer.parse(current_panel_colour)
        panel_colours[current_pos] = colour
        if computer.halted:
            break

        turn_direction = computer.parse(current_panel_colour)
        direction = update_direction(turn_direction, direction)
        increment = direction_map[direction]
        current_pos = (current_pos[0] + increment[0], current_pos[1] + increment[1])
        if computer.halted:
            break

    return panel_colours


def paint_grid(
    panel_colours: Mapping[Tuple[int, int], int],
    min_x: int,
    max_x: int,
    min_y: int,
    max_y: int,
) -> None:
    white, black = "X", " "
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print(white if panel_colours.get((x, y), False) == 1 else black, end=" ")
        print()


def main():
    data = loadv2("data/d11.txt")
    computer = Intcode()
    computer.load_data(data)
    panel_colours = paint(computer)
    x_arr = [x for x, _ in panel_colours.keys()]
    y_arr = [y for _, y in panel_colours.keys()]
    paint_grid(panel_colours, min(x_arr), max(x_arr), min(y_arr), max(y_arr))


if __name__ == "__main__":
    main()

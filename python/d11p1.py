from helper import loadv2
from intcode import Intcode


def update_direction(output: int, current_direction: str) -> str:
    directions = "URDL"
    index = directions.index(current_direction)
    increment = 1 if output else -1
    new_index = ((index + increment) + len(directions)) % len(directions)
    return directions[new_index]


def paint(computer: Intcode) -> int:
    """O is black, 1 is white"""
    BLACK, current_pos, panel_colours = 0, (0, 0), {}
    direction_map = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}
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

    return len(panel_colours.keys())


def main():
    data = loadv2("data/d11.txt")
    computer = Intcode()
    computer.load_data(data)
    n_unique_panels = paint(computer)
    return n_unique_panels


if __name__ == "__main__":
    print(main())

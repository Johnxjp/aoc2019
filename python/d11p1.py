from itertools import permutations
from typing import Sequence, Tuple
from helper import loadv2


class Intcode(list):
    def __init__(self, intcode: Sequence[int]):
        super().__init__(intcode)

    def index_check(f):
        def _check(self, idx, *args, **kwargs):
            if idx < 0:
                raise ValueError("Can't access negative values")

            if idx >= len(self):
                self += [0] * (idx - (len(self) - 1))

            return f(self, idx, *args, **kwargs)

        return _check

    @index_check
    def __getitem__(self, idx):
        return super().__getitem__(idx)

    @index_check
    def __setitem__(self, idx, o):
        super().__setitem__(idx, o)


def parse_opcode(opcode: int) -> Tuple[int, Sequence[int]]:
    params = [0] * 3
    if len(str(opcode)) <= 2:
        return opcode, params

    opcode_str = str(opcode)
    opcode = int(opcode_str[-2:])
    modes = opcode_str[:-2]
    for i, p in enumerate(reversed(modes)):
        params[i] = int(p)

    return opcode, params


def parse(intcode: Intcode, input: int, start_pointer: int = 0) -> Tuple[int, bool]:
    pointer = start_pointer
    output = float("inf")
    relative_base = 0
    while pointer < len(intcode):
        opcode = intcode[pointer]
        opcode, modes = parse_opcode(opcode)
        if opcode == 99:
            pointer += 1
            return output, pointer, True
        if opcode == 4:
            output = get_val(intcode, pointer + 1, modes[0], relative_base)
            pointer += 2
            break

        if opcode == 3:
            addr = get_addr(intcode, pointer + 1, modes[0], relative_base)
            intcode[addr] = input
            pointer += 2

        if opcode == 2 or opcode == 1:
            a = get_val(intcode, pointer + 1, modes[0], relative_base)
            b = get_val(intcode, pointer + 2, modes[1], relative_base)
            c = get_addr(intcode, pointer + 3, modes[2], relative_base)
            intcode[c] = a + b if opcode == 1 else a * b
            pointer += 4

        if opcode == 5 or opcode == 6:
            a = get_val(intcode, pointer + 1, modes[0], relative_base)
            b = get_val(intcode, pointer + 2, modes[1], relative_base)
            if a and opcode == 5:
                pointer = b
            elif not a and opcode == 6:
                pointer = b
            else:
                pointer += 3

        if opcode == 7:
            a = get_val(intcode, pointer + 1, modes[0], relative_base)
            b = get_val(intcode, pointer + 2, modes[1], relative_base)
            addr = get_addr(intcode, pointer + 3, modes[2], relative_base)
            intcode[addr] = 1 if a < b else 0
            pointer += 4

        if opcode == 8:
            a = get_val(intcode, pointer + 1, modes[0], relative_base)
            b = get_val(intcode, pointer + 2, modes[1], relative_base)
            addr = get_addr(intcode, pointer + 3, modes[2], relative_base)
            intcode[addr] = 1 if a == b else 0
            pointer += 4

        if opcode == 9:
            relative_base += get_val(intcode, pointer + 1, modes[0], relative_base)
            pointer += 2

    return output, pointer, False


def get_val(intcode: Intcode, pointer: int, mode: int, rel_base: int) -> int:
    if mode == 1:
        return intcode[pointer]

    addr = intcode[pointer] if mode == 0 else intcode[pointer] + rel_base
    return intcode[addr]


def get_addr(intcode: Intcode, pointer: int, mode: int, rel_base: int) -> int:
    if mode == 1:
        return intcode[pointer]

    return intcode[pointer] if mode == 0 else intcode[pointer] + rel_base


def update_direction(output: int, current_direction: str) -> str:
    directions = "URDL"
    index = directions.index(current_direction)
    increment = 1 if output else -1
    new_index = ((index + increment) + len(directions)) % len(directions)
    return directions[new_index]


def run_robot(intcode: Intcode) -> int:
    """O is black, 1 is white"""
    BLACK = 0
    pointer = 0
    current_pos = (0, 0)
    panel_colours = {}
    direction_map = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}
    direction = "U"
    while True:
        current_panel_colour = panel_colours.get(current_pos, BLACK)
        colour, pointer, program_ended = parse(intcode, current_panel_colour, pointer)
        panel_colours[current_pos] = colour
        if program_ended:
            break

        turn_direction, pointer, program_ended = parse(
            intcode, current_panel_colour, pointer
        )
        direction = update_direction(turn_direction, direction)
        increment = direction_map[direction]
        current_pos = (current_pos[0] + increment[0], current_pos[1] + increment[1])
        if program_ended:
            break

    return len(panel_colours.keys())


def main():
    intcode = loadv2("data/d11.txt")
    intcode = Intcode(intcode)
    n_unique_panels = run_robot(intcode)
    return n_unique_panels


if __name__ == "__main__":
    print(main())

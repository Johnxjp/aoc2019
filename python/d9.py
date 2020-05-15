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


def parse(intcode: Intcode, input: int) -> int:
    pointer = 0
    output = float("inf")
    relative_base = 0
    while pointer < len(intcode):
        opcode = intcode[pointer]
        opcode, modes = parse_opcode(opcode)
        if opcode == 99:
            break
        if opcode == 4:
            output = get_val(intcode, pointer + 1, modes[0], relative_base)
            pointer += 2

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

    return output


def get_val(intcode: Intcode, pointer: int, mode: int, rel_base: int) -> int:
    if mode == 1:
        return intcode[pointer]

    addr = intcode[pointer] if mode == 0 else intcode[pointer] + rel_base
    return intcode[addr]


def get_addr(intcode: Intcode, pointer: int, mode: int, rel_base: int) -> int:
    if mode == 1:
        return intcode[pointer]

    return intcode[pointer] if mode == 0 else intcode[pointer] + rel_base


def main():
    intcode = loadv2("data/d9.txt")
    intcode = Intcode(intcode)

    part1 = parse(intcode, 1)
    part2 = parse(intcode, 2)
    return part1, part2

if __name__ == "__main__":
    print(main())

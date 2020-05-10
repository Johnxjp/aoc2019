from typing import Sequence, Tuple
from helper import loadv2


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


def parse(intcode: Sequence[int], input: int) -> Sequence[int]:
    pointer = 0
    output = float("inf")
    while pointer < len(intcode):
        opcode = intcode[pointer]
        opcode, modes = parse_opcode(opcode)
        if opcode == 99:
            break
        if opcode == 4:
            if modes[0] == 1:
                output = intcode[pointer + 1]
            else:
                addr = intcode[pointer + 1]
                output = intcode[addr]
            pointer += 2

        if opcode == 3:
            addr = intcode[pointer + 1]
            intcode[addr] = input
            pointer += 2

        if opcode == 2 or opcode == 1:
            a = intcode[pointer + 1] if modes[0] == 1 else intcode[intcode[pointer + 1]]
            b = intcode[pointer + 2] if modes[1] == 1 else intcode[intcode[pointer + 2]]
            c = intcode[pointer + 3]
            intcode[c] = a + b if opcode == 1 else a * b
            pointer += 4

    return output


def main():
    intcode = loadv2("data/d5.txt")
    output = parse(intcode, input=1)
    return output


if __name__ == "__main__":
    print(main())

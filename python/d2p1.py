from typing import Sequence
from helper import loadv2


def parser(intcode: Sequence[int]) -> Sequence[int]:
    skip = 4
    for pointer in range(0, len(intcode), skip):
        opcode, param1, param2, param3 = intcode[pointer : pointer + skip]
        if opcode == 1:
            a, b = intcode[param1], intcode[param2]
            intcode[param3] = a + b
        elif opcode == 2:
            a, b = intcode[param1], intcode[param2]
            intcode[param3] = a * b
        elif opcode == 99:
            break
        else:
            raise ValueError("Bad Opcode")

    return intcode


def main():
    intcode = loadv2("data/d2.txt")
    intcode[1] = 12
    intcode[2] = 2
    intcode = parser(intcode)
    return intcode[0]


if __name__ == "__main__":
    print(main())

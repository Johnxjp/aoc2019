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
    target_value = 19690720
    for noun in range(100):
        for verb in range(100):
            intcode_copy = list(intcode)
            intcode_copy[1], intcode_copy[2] = noun, verb
            output = parser(intcode_copy)
            if output[0] == target_value:
                return 100 * noun + verb

    return float("inf")


if __name__ == "__main__":
    print(main())

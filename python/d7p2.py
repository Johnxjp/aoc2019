from dataclasses import dataclass
from itertools import permutations
from typing import Mapping, Optional, Sequence, Tuple
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


def parse(intcode: Sequence[int], inputs: Sequence[int]) -> Sequence[int]:
    pointer = 0
    output = float("inf")
    input_count = 0
    while pointer < len(intcode):
        opcode = intcode[pointer]
        opcode, modes = parse_opcode(opcode)
        if opcode == 99:
            return output, True
        if opcode == 4:
            if modes[0] == 1:
                output = intcode[pointer + 1]
            else:
                addr = intcode[pointer + 1]
                output = intcode[addr]
            pointer += 2

        if opcode == 3:
            addr = intcode[pointer + 1]
            try:
                intcode[addr] = inputs[input_count]
            except IndexError:
                return output, False
            input_count += 1
            pointer += 2

        if opcode == 2 or opcode == 1:
            a = intcode[pointer + 1] if modes[0] == 1 else intcode[intcode[pointer + 1]]
            b = intcode[pointer + 2] if modes[1] == 1 else intcode[intcode[pointer + 2]]
            c = intcode[pointer + 3]
            intcode[c] = a + b if opcode == 1 else a * b
            pointer += 4

        if opcode == 5 or opcode == 6:
            a = intcode[pointer + 1] if modes[0] == 1 else intcode[intcode[pointer + 1]]
            b = intcode[pointer + 2] if modes[1] == 1 else intcode[intcode[pointer + 2]]
            if a and opcode == 5:
                pointer = b
            elif not a and opcode == 6:
                pointer = b
            else:
                pointer += 3

        if opcode == 7:
            a = intcode[pointer + 1] if modes[0] == 1 else intcode[intcode[pointer + 1]]
            b = intcode[pointer + 2] if modes[1] == 1 else intcode[intcode[pointer + 2]]
            addr = intcode[pointer + 3]
            intcode[addr] = 1 if a < b else 0
            pointer += 4

        if opcode == 8:
            a = intcode[pointer + 1] if modes[0] == 1 else intcode[intcode[pointer + 1]]
            b = intcode[pointer + 2] if modes[1] == 1 else intcode[intcode[pointer + 2]]
            addr = intcode[pointer + 3]
            intcode[addr] = 1 if a == b else 0
            pointer += 4

    return output, False


@dataclass
class AmplifierStatus:
    inputs: Sequence[int]
    halted: bool = False


def amplifier_map(phases: Sequence[int]) -> Mapping[str, AmplifierStatus]:
    outputs = {}
    for amplifier, phase_value in zip("ABCDE", phases):
        outputs[amplifier] = AmplifierStatus([phase_value])

    return outputs


def max_thruster(intcode: Sequence[int]) -> int:
    phase_values = [5, 6, 7, 8, 9]
    max_output = 0
    for phase_combo in permutations(phase_values):
        output = 0
        amplifier_statuses = amplifier_map(phase_combo)
        while not amplifier_statuses["E"].halted:
            for amplifier in "ABCDE":
                amplifier_statuses[amplifier].inputs.append(output)
                output, has_halted = parse(
                    list(intcode), amplifier_statuses[amplifier].inputs
                )
                amplifier_statuses[amplifier].halted = has_halted

        max_output = max(output, max_output)

    return max_output


def main():
    intcode = loadv2("data/d7.txt")
    return max_thruster(intcode)


if __name__ == "__main__":
    print(main())

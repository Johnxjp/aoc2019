from typing import Sequence, Tuple


class Memory(list):
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


class Intcode:
    def __init__(self):
        self.memory = Memory()
        self.pointer = 0
        self.relative_base = 0
        self.halted = False
        self.last_output = None

    # Might be unecessary
    def restart(self):
        self.memory = Memory()
        self.pointer = 0
        self.relative_base = 0
        self.halted = False
        self.last_output = None

    def _parse_opcode(self, opcode: int) -> Tuple[int, Sequence[int]]:
        params = [0] * 3
        if len(str(opcode)) <= 2:
            return opcode, params

        opcode_str = str(opcode)
        opcode = int(opcode_str[-2:])
        modes = opcode_str[:-2]
        for i, p in enumerate(reversed(modes)):
            params[i] = int(p)

        return opcode, params

    def _get_val(self, pointer: int, mode: int) -> int:
        if mode == 1:
            return self.memory[pointer]

        addr = (
            self.memory[pointer]
            if mode == 0
            else self.memory[pointer] + self.relative_base
        )
        return self.memory[addr]

    def _get_addr(self, pointer: int, mode: int) -> int:
        if mode == 1:
            return self.memory[pointer]

        return (
            self.memory[pointer]
            if mode == 0
            else self.memory[pointer] + self.relative_base
        )

    def load_data(self, data: Sequence[int]) -> None:
        self.memory = Memory(data)

    def parse(self, input: int) -> int:
        """
        Parses data until output or program terminates. Returns current output.
        It will continue to parse the data from the last point if called
        subsequently. Call restart to begin again
        """
        pointer = self.pointer
        while not self.halted and pointer < len(self.memory):
            opcode = self.memory[pointer]
            opcode, modes = self._parse_opcode(opcode)
            if opcode == 99:
                pointer += 1
                self.halted = True
            if opcode == 4:
                self.last_output = self._get_val(pointer + 1, modes[0])
                pointer += 2
                break

            if opcode == 3:
                addr = self._get_addr(pointer + 1, modes[0])
                self.memory[addr] = input
                pointer += 2

            if opcode == 2 or opcode == 1:
                a = self._get_val(pointer + 1, modes[0])
                b = self._get_val(pointer + 2, modes[1])
                c = self._get_addr(pointer + 3, modes[2])
                self.memory[c] = a + b if opcode == 1 else a * b
                pointer += 4

            if opcode == 5 or opcode == 6:
                a = self._get_val(pointer + 1, modes[0])
                b = self._get_val(pointer + 2, modes[1])
                if a and opcode == 5:
                    pointer = b
                elif not a and opcode == 6:
                    pointer = b
                else:
                    pointer += 3

            if opcode == 7:
                a = self._get_val(pointer + 1, modes[0])
                b = self._get_val(pointer + 2, modes[1])
                addr = self._get_addr(pointer + 3, modes[2])
                self.memory[addr] = 1 if a < b else 0
                pointer += 4

            if opcode == 8:
                a = self._get_val(pointer + 1, modes[0])
                b = self._get_val(pointer + 2, modes[1])
                addr = self._get_addr(pointer + 3, modes[2])
                self.memory[addr] = 1 if a == b else 0
                pointer += 4

            if opcode == 9:
                self.relative_base += self._get_val(pointer + 1, modes[0])
                pointer += 2

        self.pointer = pointer
        return self.last_output

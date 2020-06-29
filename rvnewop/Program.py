from . import RV32

import sys


class Program:
    """A Program is a collection of instructions which are mapped to pc values"""

    def __init__(self, isa="32I"):
        self.rv = RV32(isa)
        self.instructions = {}  # maps pc value -> RVInstruction
        self.frequencies = {}  # maps pc value -> frequency of instruction

    def addInstruction(self, pc, hex, freq):
        """Adds an instruction to a Program given a PC value
        and the instruction hex value

        pc - (int) program counter (pc)
        hex - (str) instruction encoded in hexadecimal
        freq - (int) amount of times instruction shows up"""
        self.instructions[pc] = rv.decodeHex(hex)

        # TODO decouple storing frequencies from program?
        self.frequencies[pc] = freq

    def printAll(self, file=sys.stdout):
        """Prints out all instructions to file (default is stdout)"""
        for pc in self.program:
            print("{}: {}".format(hex(pc), self.instructions[pc]), file=file)

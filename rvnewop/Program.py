from . import RV32

import sys


class Program:
    """A Program is a collection of instructions which are mapped to pc values"""

    def __init__(self, isa="32I"):
        self.rv = RV32(isa=isa)
        self.instructions = {}  # maps pc value -> RVInstruction
        self.frequencies = {}  # maps pc value -> frequency of instruction

        # sets of names, registers, and formats for analysis
        self.instructionNameSet = set()
        self.registerSet = set()
        self.formatSet = set()

    def addInstruction(self, pc, hexd, freq):
        """Adds an instruction to a Program given a PC value
        and the instruction hex value

        pc - (int) program counter (pc)
        hexd - (str) instruction encoded in hexadecimal
        freq - (int) amount of times instruction shows up"""
        inst = self.rv.decodeHex(hexd)
        self.instructions[pc] = inst

        # add to set as you go
        self.instructionNameSet.add(inst.name)
        self.registerSet.update(set(inst.src_registers) | set(inst.dest_registers))
        self.formatSet.add(inst.format)

        # TODO decouple storing frequencies from program?
        self.frequencies[pc] = freq

    def printAll(self, file=sys.stdout):
        """Prints out all instructions to file (default is stdout)"""
        for pc in self.instructions:
            print("{}: {}".format(hex(pc), self.instructions[pc]), file=file)

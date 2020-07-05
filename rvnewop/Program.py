from . import RV32

import sys


class Program:
    """A Program is a collection of instructions which are mapped to pc values"""

    def __init__(self, isa="32I"):
        self.rv = RV32(isa=isa)
        self.instructions = {}  # maps pc value -> RVInstruction
        self.frequencies = {}  # maps pc value -> frequency of instruction
        self.instructionNameSet = None
        self.registerSet = None

    def addInstruction(self, pc, hexd, freq):
        """Adds an instruction to a Program given a PC value
        and the instruction hex value

        pc - (int) program counter (pc)
        hexd - (str) instruction encoded in hexadecimal
        freq - (int) amount of times instruction shows up"""
        self.instructions[pc] = self.rv.decodeHex(hexd)

        # TODO decouple storing frequencies from program?
        self.frequencies[pc] = freq

    def getInstructionNameSet(self):
        if not self.instructionNameSet:
            self.instructionNameSet = {
                self.instructions[pc].name for pc in self.instructions
            }
        return self.instructionNameSet

    def getRegisterSet(self):
        if not self.registerSet:
            self.registerSet = set()
            for pc in self.instructions:
                inst = self.instructions[pc]

                # update registerSet with union of registers used
                self.registerSet.update(
                    set(inst.src_registers) | set(inst.dest_registers)
                )
        return self.registerSet

    def printAll(self, file=sys.stdout):
        """Prints out all instructions to file (default is stdout)"""
        for pc in self.instructions:
            print("{}: {}".format(hex(pc), self.instructions[pc]), file=file)

from . import I32
from . import M32
from . import RVFormatParser
from . import V32
from . import C32
import sys


class RV32:
    """ General class for RISC-V 32bit """

    def __init__(self, isa="32I"):
        """ A constructor for RV32
            isa is a string containing which instruction sets and extensions to use, by default this will use 32I"""

        # a mapping from frozenbitarray of opcode --> function that returns an RVInstruction
        self.instructionTable = {}

        if "32I" in isa:
            self.instructionTable.update(I32.instructionTable)
        if "M" in isa:
            self.instructionTable.update(M32.instructionTable)
        if "V" in isa:
            self.instructionTable.update(V32.instructionTable)
        if "C" in isa:
            self.instructionTable.update(C32.instructionTable)

        # the program is a mapping from a pc int --> RVInstruction
        self.program = {}

    def decode(self, ba):
        return self.instructionTable[RVFormatParser.getOpcode(ba)](ba)

    def addInstruction(self, pc, ba):
        """ Adds Instruction from pc into program map
            pc - an integer (program counter)
            ba - the bitarray for the instruction
        """
        self.program[pc] = self.decode(ba)

    def printAll(self, file=sys.stdout):
        """ Prints out all instructions """
        for pc in self.program:
            print("{}: {}".format(hex(pc), self.program[pc]), file=file)

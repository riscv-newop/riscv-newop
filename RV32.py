from I32 import I32
from M32 import M32
from RVFormatParser import RVFormatParser


# TODO add support for M,A,C, etc
class RV32:
    """ General class for RISC-V 32bit """

    def __init__(self, isa="32I"):
        """ A constructor for RV32
            isa is a string containing which instruction sets and extensions to use, by default this will use 32I"""
        self.instructionTable = {}

        if "32I" in isa:
            self.instructionTable.update(I32.instructionTable)
        if "M" in isa:
            self.instructionTable.update(M32.instructionTable)

        self.program = {}  # key is pc, value is RVInstruction

    def addInstruction(self, pc, ba):
        """ Adds Instruction from pc into program """
        self.program[pc] = self.instructionTable[RVFormatParser.getOpcode(ba)](ba)

    def printAll(self):
        """ Prints out all instructions """
        for pc in self.program:
            print("{}: {}".format(pc, self.program[pc]))

from I32 import I32
from M32 import M32
from V32 import V32	#NEW
from RVFormatParser import RVFormatParser


class RV32:
    """ General class for RISC-V 32bit """

    def __init__(self, isa="V"):
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

        # the program is a mapping from a pc int --> RVInstruction
        self.program = {}

    def addInstruction(self, pc, ba):
        """ Adds Instruction from pc into program map
            pc - an integer (program counter)
            ba - the bitarray for the instruction
        """
        self.program[pc] = self.instructionTable[RVFormatParser.getOpcode(ba)](ba)

    def printAll(self):
        """ Prints out all instructions """
        for pc in self.program:
            print("{}: {}".format(pc, self.program[pc]))

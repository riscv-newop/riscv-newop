from I32 import I32
from RVFormatParser import RVFormatParser

# TODO add support for M,A,C, etc
# TODO accept
class RV32(I32):
    """ General class for RISC-V 32bit """

    def __init__():
        self.instructionTable = I32.instructionTable
        self.program = {} # key is pc, value is RVInstruction

    def addInstruction(self, pc, ba):
        """ Adds Instruction from pc into program """
        self.program[pc] = self.instructionTable[RVFormatParser.getOpcode(ba)](ba)

    def printAll(self):
        for pc in self.program:
            print("{}: {}".format(pc, self.program[pc]))

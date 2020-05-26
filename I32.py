from RVInstructionSet import RVInstructionSet
from RVInstruction import RVInstruction
from bitarray import frozenbitarray


class I32(RVInstructionSet):
    """A class that implements the RV32I base instruction set"""

    # TODO
    @staticmethod
    def LUI():
        pass

    # TODO
    @staticmethod
    def AUIPC():
        pass

    # TODO
    @staticmethod
    def JAL():
        pass

    # TODO
    @staticmethod
    def JALR():
        pass

    # TODO
    @staticmethod
    def BRANCHES():
        pass

    # TODO
    @staticmethod
    def LOAD():
        pass

    # TODO
    @staticmethod
    def STORE():
        pass

    # TODO
    @staticmethod
    def IMMEDIATE():
        pass

    # TODO
    @staticmethod
    def REGISTER():
        pass

    @staticmethod
    def ECALL():
        return RVInstruction(rv_name="ecall", rv_size=32)

    @staticmethod
    def EBREAK():
        return RVInstruction(rv_name="ebreak", rv_size=32)

    def __init__(self):
        self.instructionTable = {
            frozenbitarray("0110111"): LUI,
            frozenbitarray("0010111"): AUIPC,
            frozenbitarray("1101111"): JAL,
            frozenbitarray("1100111"): JALR,
            frozenbitarray("1100011"): BRANCHES,  # branch instructions
            frozenbitarray("0000011"): LOAD,  # load instructions
            frozenbitarray("0100011"): STORE,  # store instructions
            frozenbitarray("0010011"): IMMEDIATE,  # register immediate instructions
            frozenbitarray("0110011"): REGISTER,  # register register instructions
            frozenbitarray("1110011"): ECALL,
            frozenbitarray("1110011"): EBREAK,
        }

    @property
    def instructionTable(self):
        return self.instructionTable

from bitarray import frozenbitarray

from RVFormatParser import RVFormatParser as fp
from RVInstruction import RVInstruction
from RVInstructionSet import RVInstructionSet


class I32(RVInstructionSet):
    """A class that implements the RV32I base instruction set"""

    @staticmethod
    def LUI(ba):
        """Creates 'Load Upper Immediate' Instruction"""
        data = fp.parseU(ba)
        return RVInstruction(
            rv_format="U",
            rv_dest_registers=[data["rd"]],
            rv_immediates=[data["imm"]],
            rv_name="lui",
            rv_size=32,
            rv_binary=ba,
        )

    @staticmethod
    def AUIPC(ba):
        """Creates 'Add Upper Immediate to PC' Instruction"""
        data = fp.parseU(ba)
        return RVInstruction(
            rv_format="U",
            rv_dest_registers=[data["rd"]],
            rv_immediates=[data["imm"]],
            rv_name="auipc",
            rv_size=32,
            rv_binary=ba,
        )

    @staticmethod
    def JAL(ba):
        """Creates 'Jump And Link' Instruction"""
        data = fp.parseJ(ba)
        return RVInstruction(
            rv_format="J",
            rv_dest_registers=[data["rd"]],
            rv_immediates=[data["imm"]],
            rv_name="jal",
            rv_size=32,
            rv_binary=ba,
        )

    @staticmethod
    def JALR(ba):
        """Creates 'Jump And Link Register' Instruction"""
        data = fp.parseI(ba)
        return RVInstruction(
            rv_format="I",
            rv_src_registers=[data["rs1"]],
            rv_dest_registers=[data["rd"]],
            rv_immediates=[data["imm"]],
            rv_name="jalr",
            rv_size=32,
            rv_binary=ba,
        )

    @staticmethod
    def BRANCHES(ba):
        """Creates various branch Instructions"""
        data = fp.parseB(ba)
        f3 = data["funct3"]
        name = ""
        if f3 == bitarray("000"):
            # BEQ
            name = "beq"
        elif f3 == bitarray("001"):
            # BNE
            name = "bne"
        elif f3 == bitarray("100"):
            # BLT
            name = "blt"
        elif f3 == bitarray("101"):
            # BGE
            name = "bge"
        elif f3 == bitarray("110"):
            # BLTU
            name = "bltu"
        elif f3 == bitarray("111"):
            # BGEU
            name = "bgeu"
        else:
            # TODO error??
            pass

        return RVInstruction(
            rv_format="B",
            rv_src_registers=[data["rs1"], data["rs2"]],
            rv_immediates=[data["imm"]],
            rv_name=name,
            rv_size=32,
            rv_binary=ba,
        )

    # TODO
    @staticmethod
    def LOAD(ba):
        pass

    # TODO
    @staticmethod
    def STORE(ba):
        pass

    # TODO
    @staticmethod
    def IMMEDIATE(ba):
        pass

    # TODO
    @staticmethod
    def REGISTER(ba):
        pass

    @staticmethod
    def ECALL(ba):
        return RVInstruction(rv_name="ecall", rv_size=32, rv_binary=ba)

    @staticmethod
    def EBREAK(ba):
        return RVInstruction(rv_name="ebreak", rv_size=32, rv_binary=ba)

    def __init__(self):
        """Initializing the ISA instruction table"""

        self.instructionTable = {
            frozenbitarray("0110111"): LUI,
            frozenbitarray("0010111"): AUIPC,
            frozenbitarray("1101111"): JAL,
            frozenbitarray("1100111"): JALR,
            frozenbitarray("1100011"): BRANCHES,
            frozenbitarray("0000011"): LOAD,
            frozenbitarray("0100011"): STORE,
            frozenbitarray("0010011"): IMMEDIATE,
            frozenbitarray("0110011"): REGISTER,
            frozenbitarray("1110011"): ECALL,
            frozenbitarray("1110011"): EBREAK,
        }

    @property
    def instructionTable(self):
        return self.instructionTable

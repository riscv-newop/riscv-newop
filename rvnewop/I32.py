from bitarray import bitarray, frozenbitarray

from . import RVFormatParser as fp
from . import RVInstruction


class I32:
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
        """Creates various Branch Instructions"""
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

    @staticmethod
    def LOAD(ba):
        """Creates various Load Instructions"""
        data = fp.parseI(ba)
        f3 = data["funct3"]
        name = ""

        if f3 == bitarray("000"):
            # LB
            name = "lb"
        elif f3 == bitarray("001"):
            # LH
            name = "lh"
        elif f3 == bitarray("010"):
            # LW
            name = "lw"
        elif f3 == bitarray("100"):
            # LBU
            name = "lbu"
        elif f3 == bitarray("101"):
            # LHU
            name = "lhu"
        else:
            # TODO error??
            pass

        return RVInstruction(
            rv_format="I",
            rv_src_registers=[data["rs1"]],
            rv_dest_registers=[data["rd"]],
            rv_immediates=[data["imm"]],
            rv_name=name,
            rv_size=32,
            rv_binary=ba,
        )

    @staticmethod
    def STORE(ba):
        """Create various Store Instructions"""
        data = fp.parseS(ba)
        f3 = data["funct3"]
        name = ""

        if f3 == bitarray("000"):
            # SB
            name = "sb"
        elif f3 == bitarray("001"):
            # SH
            name = "sh"
        elif f3 == bitarray("010"):
            # SW
            name = "sw"
        else:
            # TODO error??
            pass

        return RVInstruction(
            rv_format="S",
            rv_src_registers=[data["rs1"], data["rs2"]],
            rv_immediates=[data["imm"]],
            rv_name=name,
            rv_size=32,
            rv_binary=ba,
        )

    @staticmethod
    def IMMEDIATE(ba):
        """Creates various Register Immediate Instructions"""
        data = fp.parseI(ba, convert=False)
        f3 = data["funct3"]
        name = ""
        shift = False
        imm = None

        if f3 == bitarray("000"):
            # ADDI
            name = "addi"
        elif f3 == bitarray("010"):
            # SLTI
            name = "slti"
        elif f3 == bitarray("011"):
            # SLTIU
            name = "sltiu"
        elif f3 == bitarray("100"):
            # XORI
            name = "xori"
        elif f3 == bitarray("110"):
            # ORI
            name = "ori"
        elif f3 == bitarray("111"):
            # ANDI
            name = "andi"
        elif f3 == bitarray("001"):
            # SLLI
            name = "slli"
            shift = True

        # These two share the same funct3 value
        # but have a different 2nd to most significant bit
        elif f3 == bitarray("101"):
            if data["imm"][1] == 0:
                # SRLI
                name = "srli"
            else:
                # SRAI
                name = "srai"
            shift = True

        if shift:
            # to account for the shamt, shift amount
            imm = fp.immToInt(data["imm"][7:])
        else:
            # for every other immediate instruction
            imm = fp.immToInt(bitarray(data["imm"]))

        return RVInstruction(
            rv_format="I",
            rv_src_registers=[data["rs1"]],
            rv_dest_registers=[data["rd"]],
            rv_immediates=[imm],
            rv_name=name,
            rv_size=32,
            rv_binary=ba,
        )

    @staticmethod
    def REGISTER(ba):
        """Creates Register to Register Instructions"""
        data = fp.parseR(ba)
        f3 = data["funct3"]
        f7 = data["funct7"]
        name = ""

        if f3 == bitarray("000"):
            if f7[1] == 0:
                # ADD
                name = "add"
            elif f7[1] == 1:
                # SUB
                name = "sub"
        elif f3 == bitarray("001"):
            # SLL
            name = "sll"
        elif f3 == bitarray("010"):
            # SLT
            name = "slt"
        elif f3 == bitarray("011"):
            # SLTU
            name = "sltu"
        elif f3 == bitarray("100"):
            # XOR
            name = "xor"
        elif f3 == bitarray("101"):
            if f7[1] == 0:
                # SRL
                name = "srl"
            elif f7[1] == 1:
                # SRA
                name = "sra"
        elif f3 == bitarray("110"):
            # OR
            name = "or"
        elif f3 == bitarray("111"):
            # AND
            name = "and"
        else:
            # TODO error??
            pass

        return RVInstruction(
            rv_format="R",
            rv_src_registers=[data["rs1"], data["rs2"]],
            rv_dest_registers=[data["rd"]],
            rv_name=name,
            rv_size=32,
            rv_binary=ba,
        )

    @staticmethod
    def ENVIRONMENT(ba):
        data = fp.parseI(ba)
        name = "ecall" if data["imm"] == 0 else "ebreak"
        return RVInstruction(rv_name=name, rv_size=32, rv_binary=ba)

    @staticmethod
    def FENCE(ba):
        # TODO actually implement, this is just here to prevent errors
        return RVInstruction(rv_name="fence", rv_size=32, rv_binary=ba)

    # dictionary of opcodes --> functions(bitarray) --> RVInstruction
    instructionTable = {
        frozenbitarray("0110111"): LUI.__func__,
        frozenbitarray("0010111"): AUIPC.__func__,
        frozenbitarray("1101111"): JAL.__func__,
        frozenbitarray("1100111"): JALR.__func__,
        frozenbitarray("1100011"): BRANCHES.__func__,
        frozenbitarray("0000011"): LOAD.__func__,
        frozenbitarray("0100011"): STORE.__func__,
        frozenbitarray("0010011"): IMMEDIATE.__func__,
        frozenbitarray("0110011"): REGISTER.__func__,
        frozenbitarray("1110011"): ENVIRONMENT.__func__,
        frozenbitarray("0001111"): FENCE.__func__,
    }

    instructionNameSet = {
        "lui",
        "auipc",
        "jal",
        "jalr",
        "beq",
        "bne",
        "blt",
        "bge",
        "bltu",
        "bgeu",
        "lb",
        "lh",
        "lw",
        "lbu",
        "lhu",
        "sb",
        "sh",
        "sw",
        "addi",
        "slti",
        "sltiu",
        "xori",
        "ori",
        "andi",
        "slli",
        "srli",
        "srai",
        "add",
        "sub",
        "sll",
        "slt",
        "sltu",
        "xor",
        "srl",
        "sra",
        "or",
        "and",
        "ecall",
        "ebreak",
        "fence",
    }

    # Registers used in this isa
    registerSet = {"x{}".format(i) for i in range(32)}

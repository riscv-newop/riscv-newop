from bitarray import bitarray, frozenbitarray

from . import RVFormatParser as fp
from . import RVInstruction


class M32:
    """ A Class implementing the RV32M Standard Extension """

    @staticmethod
    def MULTIPLY(ba):
        data = fp.parseR(ba)
        f3 = data["funct3"]
        name = ""

        if f3 == bitarray("000"):
            # MUL
            name = "mul"
        elif f3 == bitarray("001"):
            # MULH
            name = "mulh"
        elif f3 == bitarray("010"):
            # MULHSU
            name = "MULHSU"
        elif f3 == bitarray("011"):
            # MULHU
            name = "mulhu"
        elif f3 == bitarray("100"):
            # DIV
            name = "div"
        elif f3 == bitarray("101"):
            # DIVU
            name = "divu"
        elif f3 == bitarray("110"):
            # REM
            name = "rem"
        elif f3 == bitarray("111"):
            # REMU
            name = "remu"
        else:
            # TODO error
            pass

        return RVInstruction(
            rv_format="R",
            rv_src_registers=[data["rs1"], data["rs2"]],
            rv_dest_registers=[data["rd"]],
            rv_name=name,
            rv_size=32,
            rv_binary=ba,
        )

    instructionTable = {
        frozenbitarray("0110011"): MULTIPLY.__func__,
    }

    instructionNameSet = {
        "mul",
        "mulh",
        "MULHSU",
        "mulhu",
        "div",
        "divu",
        "rem",
        "remu",
    }

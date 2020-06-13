from bitarray import bitarray, frozenbitarray
from bitarray.util import zeros

from RVFormatParser import RVFormatParser as fp
from RVInstruction import RVInstruction


class C32:
    """ A Class implementing the RV32I Compressed Standard Extension """

    @staticmethod
    def QUADRANT_0(ba):
        if ba == zeros(16):
            # illegal instructions are all 0s
            return RVInstruction(rv_name="illegal")

        f3 = fp.getCOpcode(ba)

        if f3 == "000":
            # C.ADDI4SPN
            data = fp.parseCIW(ba)
            imm = data["imm"]

            return RVInstruction(
                rv_format="CIW",
                rv_src_registers=["x2"],
                rv_dest_registers=[data["rd_pop"]],
                rv_immediates=RVFormatParser.immToInt(
                    imm[2:6] + imm[:2] + bitarray(imm[-1]) + bitarray(imm[-2])
                )
                * 4,
                rv_name="c.addi4spn",
                rv_size=16,
                rv_binary=ba,
            )

        elif f3 == "001":
            # C.FLD, not implemented
            pass

        elif f3 == "010":
            # C.LW
            pass

        elif f3 == "011":
            # C.FLW, not implemented
            pass

        elif f3 == "100":
            # RESERVED
            pass

        elif f3 == "101":
            # C.FSD, not implemented
            pass

        elif f3 == "110":
            # C.SW
            pass

        elif f3 == "111":
            # C.FSW, not implemented
            pass

    @staticmethod
    def QUADRANT_1(ba):
        pass

    @staticmethod
    def QUADRANT_2(ba):
        pass

    instructionTable = {
        frozenbitarray("00"): QUADRANT_0.__func__,
        frozenbitarray("01"): QUADRANT_1.__func__,
        frozenbitarray("10"): QUADRANT_2.__func__,
    }

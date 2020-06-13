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

        f3 = fp.getCFunct3(ba)

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
            data = fp.parseCL(ba)
            imm3 = data["imm3"]
            imm2 = data["imm2"]
            return RVInstruction(
                rv_format="CL",
                rv_src_registers=[data["rs1_pop"]],
                rv_dest_registers=[data["rd_pop"]],
                rv_immediates=RVFormatParser.immToInt(
                    bitarray(imm2[1]) + imm3 + bitarray(imm2[0])
                )
                * 4,
                rv_name="c.lw",
                rv_size=16,
                rv_binary=ba,
            )

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
            data = fp.parseCS(ba)
            imm3 = data["imm3"]
            imm2 = data["imm2"]
            return RVInstruction(
                rv_format="CS",
                rv_src_registers=[data["rs1_pop"], data["rs2_pop"]],
                rv_immediates=RVFormatParser.immToInt(
                    bitarray(imm2[1]) + imm3 + bitarray(imm2[0])
                )
                * 4,
                rv_name="c.lw",
                rv_size=16,
                rv_binary=ba,
            )
        elif f3 == "111":
            # C.FSW, not implemented
            pass

    @staticmethod
    def QUADRANT_1(ba):
        f3 = fp.getCFunct3(ba)

        if f3 == "000":
            # C.NOP or C.ADDI
            data = fp.parseCI(ba)
            imm = data["imm1"] + data["imm5"]

            if data["register"] == zeros(5):
                # C.NOP
                return RVInstruction(
                    rv_format="CI",
                    rv_immediates=RVFormatParser.immToInt(imm),
                    rv_name="c.nop",
                    rv_size=16,
                    rv_binary=ba,
                )
            else:
                # C.ADDI
                return RVInstruction(
                    rv_format="CI",
                    rv_src_registers=[data["register"]],
                    rv_dest_registers=[data["register"]],
                    rv_immediates=RVFormatParser.immToInt(imm),
                    rv_name="c.addi",
                    rv_size=16,
                    rv_binary=ba,
                )

        elif f3 == "001":
            # C.JAL
            data = fp.parseCJ(ba)
            jump_t = data["jump_target"]

            imm = (
                bitarray(jump_t[0])  # 11
                + bitarray(jump_t[4])  # 10
                + jump_t[2:4]  # 9:8
                + bitarray(jump_t[6])  # 7
                + bitarray(jump_t[5])  # 6
                + bitarray(jump_t[10])  # 5
                + bitarray(jump_t[1])  # 4
                + jump_t[7:10]  # 3:1
                + bitarray("0")  # 0, as it is left shifted 2
            )

            return RVInstruction(
                rv_format="CJ",
                rv_dest_registers=["x1"],
                rv_immediates=RVFormatParser.immToInt(imm),
                rv_name="c.jal",
                rv_size=16,
                rv_binary=ba,
            )

        elif f3 == "010":
            # C.LI
            pass

        elif f3 == "011":
            # C.ADDI16SP or C.LUI
            pass

        elif f3 == "100":
            # C.SRLI, C.SRAI, C.ANDI, C.SUB, C.XOR, C.OR, C.AND
            pass

        elif f3 == "101":
            # C.J
            data = fp.parseCJ(ba)
            jump_t = data["jump_target"]

            # same format as C.JAL
            imm = (
                bitarray(jump_t[0])  # 11
                + bitarray(jump_t[4])  # 10
                + jump_t[2:4]  # 9:8
                + bitarray(jump_t[6])  # 7
                + bitarray(jump_t[5])  # 6
                + bitarray(jump_t[10])  # 5
                + bitarray(jump_t[1])  # 4
                + jump_t[7:10]  # 3:1
                + bitarray("0")  # 0, as it is left shifted 2
            )

            return RVInstruction(
                rv_format="CJ",
                rv_dest_registers=["x0"],
                rv_immediates=RVFormatParser.immToInt(imm),
                rv_name="c.j",
                rv_size=16,
                rv_binary=ba,
            )

        elif f3 == "110":
            # C.BEQZ
            pass

        elif f3 == "111":
            # C.BNEZ
            pass

    @staticmethod
    def QUADRANT_2(ba):
        pass

    instructionTable = {
        frozenbitarray("00"): QUADRANT_0.__func__,
        frozenbitarray("01"): QUADRANT_1.__func__,
        frozenbitarray("10"): QUADRANT_2.__func__,
    }

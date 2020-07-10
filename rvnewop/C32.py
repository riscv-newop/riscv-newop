from bitarray import bitarray, frozenbitarray
from bitarray.util import zeros

# from RVFormatParser import RVFormatParser as fp
from . import RVFormatParser as fp
from . import RVInstruction


class C32:
    """ A Class implementing the RV32I Compressed Standard Extension """

    @staticmethod
    def QUADRANT_0(ba):
        if ba == zeros(16):
            # illegal instructions are all 0s
            return RVInstruction(rv_name="illegal", rv_size=16)

        f3 = fp.getCFunct3(ba)

        if f3 == bitarray("000"):
            # C.ADDI4SPN
            data = fp.parseCIW(ba)
            imm = data["imm"]

            return RVInstruction(
                rv_format="CIW",
                rv_src_registers=["x2"],
                rv_dest_registers=[data["rd_pop"]],
                rv_immediates=[
                    fp.immToInt(
                        imm[2:6] + imm[:2] + bitarray([imm[-1]]) + bitarray([imm[-2]])
                    )
                    * 4
                ],
                rv_name="c.addi4spn",
                rv_size=16,
                rv_binary=ba,
            )

        elif f3 == bitarray("001"):
            # C.FLD, not implemented
            pass

        elif f3 == bitarray("010"):
            # C.LW
            data = fp.parseCL(ba)
            imm3 = data["imm3"]
            imm2 = data["imm2"]
            return RVInstruction(
                rv_format="CL",
                rv_src_registers=[data["rs1_pop"]],
                rv_dest_registers=[data["rd_pop"]],
                rv_immediates=[
                    fp.immToInt(bitarray([imm2[1]]) + imm3 + bitarray([imm2[0]])) * 4
                ],
                rv_name="c.lw",
                rv_size=16,
                rv_binary=ba,
            )

        elif f3 == bitarray("011"):
            # C.FLW, not implemented
            pass

        elif f3 == bitarray("100"):
            return RVInstruction(rv_name="reserved", rv_size=16)

        elif f3 == bitarray("101"):
            # C.FSD, not implemented
            pass

        elif f3 == bitarray("110"):
            # C.SW
            data = fp.parseCS(ba)
            imm3 = data["imm3"]
            imm2 = data["imm2"]
            return RVInstruction(
                rv_format="CS",
                rv_src_registers=[data["rs1_pop"], data["rs2_pop"]],
                rv_immediates=[
                    fp.immToInt(bitarray([imm2[1]]) + imm3 + bitarray([imm2[0]])) * 4
                ],
                rv_name="c.sw",
                rv_size=16,
                rv_binary=ba,
            )
        elif f3 == bitarray("111"):
            # C.FSW, not implemented
            pass

    @staticmethod
    def QUADRANT_1(ba):
        f3 = fp.getCFunct3(ba)

        if f3 == bitarray("000"):
            # C.NOP or C.ADDI
            data = fp.parseCI(ba)
            imm = data["imm1"] + data["imm5"]

            if data["register"] == zeros(5):
                # C.NOP
                return RVInstruction(
                    rv_format="CI",
                    rv_immediates=[fp.immToInt(imm)],
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
                    rv_immediates=[fp.immToInt(imm)],
                    rv_name="c.addi",
                    rv_size=16,
                    rv_binary=ba,
                )

        elif f3 == bitarray("001"):
            # C.JAL
            data = fp.parseCJ(ba)
            jump_t = data["jump_target"]

            imm = (
                bitarray([jump_t[0]])  # 11
                + bitarray([jump_t[4]])  # 10
                + jump_t[2:4]  # 9:8
                + bitarray([jump_t[6]])  # 7
                + bitarray([jump_t[5]])  # 6
                + bitarray([jump_t[10]])  # 5
                + bitarray([jump_t[1]])  # 4
                + jump_t[7:10]  # 3:1
                + bitarray("0")  # 0, as it is left shifted 2
            )

            return RVInstruction(
                rv_format="CJ",
                rv_dest_registers=["x1"],
                rv_immediates=[fp.immToInt(imm)],
                rv_name="c.jal",
                rv_size=16,
                rv_binary=ba,
            )

        elif f3 == bitarray("010"):
            # C.LI
            data = fp.parseCI(ba)
            imm = data["imm1"] + data["imm5"]
            if data["register"] == "x0":
                # TODO something with HINT?
                pass

            return RVInstruction(
                rv_format="CI",
                rv_dest_registers=[data["register"]],
                rv_immediates=[fp.immToInt(imm)],
                rv_name="c.li",
                rv_size=16,
                rv_binary=ba,
            )

        elif f3 == bitarray("011"):
            # C.ADDI16SP or C.LUI
            data = fp.parseCI(ba)
            imm1 = data["imm1"]
            imm5 = data["imm5"]

            if data["register"] == "x2":
                # C.ADDI16SP

                nzimm = (
                    imm1
                    + imm5[2:4]
                    + bitarray([imm5[1]])
                    + bitarray([imm5[4]])
                    + bitarray([imm5[0]])
                )

                return RVInstruction(
                    rv_format="CI",
                    rv_src_registers=["x2"],
                    rv_dest_registers=[data["register"]],
                    rv_immediates=[
                        fp.immToInt(nzimm) * 16
                    ],  # left shift by 4 (multiplying by 16)
                    rv_name="c.addi16sp",
                    rv_size=16,
                    rv_binary=ba,
                )
            else:
                # C.LUI

                nzimm = imm1 + imm5 + zeros(12)
                imm = fp.immToInt(nzimm)

                if data["register"] == "x0":
                    raise Exception("C.LUI cannot have a destination register of x0")
                if imm == 0:
                    return RVInstruction(rv_name="reserved", rv_size=16)

                return RVInstruction(
                    rv_format="CI",
                    rv_dest_registers=[data["register"]],
                    rv_immediates=[imm],
                    rv_name="c.lui",
                    rv_size=16,
                    rv_binary=ba,
                )

        elif f3 == bitarray("100"):
            # C.SRLI, C.SRAI, C.ANDI, C.SUB, C.XOR, C.OR, C.AND
            f2 = ba[-12:-10]
            if f2 == "00":
                # C.SRLI
                data = fp.parseCB(ba)
                if data["offset3"][0] == "1":
                    # TODO? reserved for custom instructions
                    return RVInstruction(rv_name="reserved", rv_size=16)

                shamt = bitarray([data["offset3"][0]]) + data["offset5"]
                return RVInstruction(
                    rv_format="CB",
                    rv_src_registers=[data["rs1_pop"]],
                    rv_dest_registers=[data["rs1_pop"]],
                    rv_immediates=[fp.immToInt(shamt)],
                    rv_name="c.srli",
                    rv_size=16,
                    rv_binary=ba,
                )
            elif f2 == bitarray("01"):
                # C.SRAI
                data = fp.parseCB(ba)
                if data["offset3"][0] == "1":
                    # TODO? reserved for custom instructions
                    return RVInstruction(rv_name="reserved", rv_size=16)

                shamt = bitarray([data["offset3"][0]]) + data["offset5"]
                return RVInstruction(
                    rv_format="CB",
                    rv_src_registers=[data["rs1_pop"]],
                    rv_dest_registers=[data["rs1_pop"]],
                    rv_immediates=[fp.immToInt(shamt)],
                    rv_name="c.srai",
                    rv_size=16,
                    rv_binary=ba,
                )
            elif f2 == bitarray("10"):
                # C.ANDI
                data = fp.parseCB(ba)

                imm = bitarray([data["offset3"][0]]) + data["offset5"]
                return RVInstruction(
                    rv_format="CB",
                    rv_src_registers=[data["rs1_pop"]],
                    rv_dest_registers=[data["rs1_pop"]],
                    rv_immediates=[fp.immToInt(imm)],
                    rv_name="c.andi",
                    rv_size=16,
                    rv_binary=ba,
                )
            elif f2 == bitarray("11"):
                # C.SUB, C.XOR, C.OR, and C.AND
                data = fp.parseCA(ba)
                funct2 = fp.getCFunct2(ba)
                name = ""
                if funct2 == bitarray("00"):
                    # C.SUB
                    name = "c.sub"
                elif funct2 == bitarray("01"):
                    # C.XOR
                    name = "c.xor"
                elif funct2 == bitarray("10"):
                    # C.OR
                    name = "c.or"
                elif funct2 == bitarray("11"):
                    # C.AND
                    name = "c.and"

                return RVInstruction(
                    rv_format="CA",
                    rv_src_registers=[data["register_pop"], data["rs2_pop"]],
                    rv_dest_registers=[data["register_pop"]],
                    rv_name=name,
                    rv_size=16,
                    rv_binary=ba,
                )

        elif f3 == bitarray("101"):
            # C.J
            data = fp.parseCJ(ba)
            jump_t = data["jump_target"]

            # same format as C.JAL
            imm = (
                bitarray([jump_t[0]])  # 11
                + bitarray([jump_t[4]])  # 10
                + jump_t[2:4]  # 9:8
                + bitarray([jump_t[6]])  # 7
                + bitarray([jump_t[5]])  # 6
                + bitarray([jump_t[10]])  # 5
                + bitarray([jump_t[1]])  # 4
                + jump_t[7:10]  # 3:1
                + bitarray("0")  # 0, as it is left shifted 2
            )

            return RVInstruction(
                rv_format="CJ",
                rv_dest_registers=["x0"],
                rv_immediates=[fp.immToInt(imm)],
                rv_name="c.j",
                rv_size=16,
                rv_binary=ba,
            )

        elif f3 == bitarray("110"):
            # C.BEQZ
            data = fp.parseCB(ba)
            offset3 = data["offset3"]
            offset5 = data["offset5"]
            offset = (
                bitarray([offset3[0]])
                + offset5[:2]
                + bitarray([offset5[4]])
                + offset3[1:]
                + offset5[2:4]
                + bitarray("0")
            )

            return RVInstruction(
                rv_format="CB",
                rv_src_registers=[data["rs1_pop"]],
                rv_immediates=[fp.immToInt(offset)],
                rv_name="c.beqz",
                rv_size=16,
                rv_binary=ba,
            )

        elif f3 == bitarray("111"):
            # C.BNEZ
            data = fp.parseCB(ba)
            offset3 = data["offset3"]
            offset5 = data["offset5"]
            offset = (
                bitarray([offset3[0]])
                + offset5[:2]
                + bitarray([offset5[4]])
                + offset3[1:]
                + offset5[2:4]
                + bitarray("0")
            )

            return RVInstruction(
                rv_format="CB",
                rv_src_registers=[data["rs1_pop"]],
                rv_immediates=[fp.immToInt(offset)],
                rv_name="c.bnez",
                rv_size=16,
                rv_binary=ba,
            )

    @staticmethod
    def QUADRANT_2(ba):
        f3 = fp.getCFunct3(ba)

        if f3 == bitarray("000"):
            # C.SLLI
            data = fp.parseCI(ba)
            imm = data["imm1"] + data["imm5"]

            return RVInstruction(
                rv_format="CI",
                rv_src_registers=[data["register"]],
                rv_dest_registers=[data["register"]],
                rv_immediates=[fp.immToInt(imm)],
                rv_name="c.slli",
                rv_size=16,
                rv_binary=ba,
            )

        elif f3 == bitarray("001"):
            # C.FLDSP, not implemented here
            pass
        elif f3 == bitarray("010"):
            # C.LWSP
            data = fp.parseCI(ba)
            imm1 = data["imm1"]
            imm5 = data["imm5"]
            imm = imm5[3:] + imm1 + imm5[:3] + zeros(2)

            return RVInstruction(
                rv_format="CI",
                rv_src_registers=["x2"],
                rv_dest_registers=[data["register"]],
                rv_immediates=[fp.immToInt(imm)],
                rv_name="c.lwsp",
                rv_size=16,
                rv_binary=ba,
            )

        elif f3 == bitarray("011"):
            # C.FLWSP, not implemented here
            pass
        elif f3 == bitarray("100"):
            # C.JR, C.MV, C.EBREAK, C.JALR, and C.ADD
            bit12 = bitarray([ba[-13]])
            data = fp.parseCR(ba)  # all of these are CR format
            if bit12 == bitarray("0"):
                # C.JR or C.MV
                if data["rs2"] == "x0":
                    # C.JR
                    return RVInstruction(
                        rv_format="CR",
                        rv_src_registers=[data["rs2"], data["register"]],
                        rv_name="c.jr",
                        rv_size=16,
                        rv_binary=ba,
                    )
                else:
                    # C.MV
                    return RVInstruction(
                        rv_format="CR",
                        rv_src_registers=["x0", data["rs2"]],
                        rv_dest_registers=[data["register"]],
                        rv_name="c.mv",
                        rv_size=16,
                        rv_binary=ba,
                    )
            else:
                # C.EBREAK, C.JALR, and C.ADD
                if data["rs2"] == "x0" and data["register"] == "x0":
                    # C.EBREAK
                    return RVInstruction(
                        rv_format="CR", rv_name="c.ebreak", rv_size=16, rv_binary=ba,
                    )
                elif data["rs2"] == "x0":
                    # C.JALR
                    return RVInstruction(
                        rv_format="CR",
                        rv_src_registers=[data["register"]],
                        rv_dest_registers=["x1"],
                        rv_name="c.jalr",
                        rv_size=16,
                        rv_binary=ba,
                    )
                else:
                    # C.ADD
                    return RVInstruction(
                        rv_format="CR",
                        rv_src_registers=[data["register"], data["rs2"]],
                        rv_dest_registers=[data["register"]],
                        rv_name="c.add",
                        rv_size=16,
                        rv_binary=ba,
                    )

        elif f3 == bitarray("101"):
            # C.FSDSP, not implemented here
            pass
        elif f3 == bitarray("110"):
            # C.SWSP
            data = fp.parseCSS(ba)
            imm = data["imm"]
            offset = fp.immToInt(imm[4:] + imm[:4] + zeros(2))

            return RVInstruction(
                rv_format="CR",
                rv_src_registers=[data["rs2"]],
                rv_immediates=[offset],
                rv_name="c.swsp",
                rv_size=16,
                rv_binary=ba,
            )

        elif f3 == bitarray("111"):
            # C.FSWSP, not implemented here
            pass

    instructionTable = {
        frozenbitarray("00"): QUADRANT_0.__func__,
        frozenbitarray("01"): QUADRANT_1.__func__,
        frozenbitarray("10"): QUADRANT_2.__func__,
    }

    instructionNameSet = {
        "c.addi4spn",
        "c.lw",
        "c.lw",
        "c.nop",
        "c.addi",
        "c.jal",
        "c.li",
        "c.addi16sp",
        "c.lui",
        "c.srli",
        "c.srai",
        "c.andi",
        "c.sub",
        "c.xor",
        "c.or",
        "c.and",
        "c.j",
        "c.beqz",
        "c.bnez",
        "c.slli",
        "c.lwsp",
        "c.jr",
        "c.mv",
        "c.ebreak",
        "c.jalr",
        "c.add",
        "c.swsp",
    }

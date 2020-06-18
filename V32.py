# TODO add rv_name for all the returns
# TODO add all the funct6's listed in the spec

from bitarray import bitarray, frozenbitarray

from RVFormatParser import RVFormatParser as fp
from RVInstruction import RVInstruction


class V32:
    """ A Class implementing the RV32V Standard Extension """

    @staticmethod
    def LOAD_FP(ba):
        """Creates Vector Load Instructions"""
        nf = ""
        width = ""
        sign = ""
        umop = ""
        vm = ""

        if (
            fp.getFunct3(ba) == bitarray("001")
            or fp.getFunct3(ba) == bitarray("010")
            or fp.getFunct3(ba) == bitarray("011")
            or fp.getFunct3(ba) == bitarray("100")
        ):
            width = ""
        elif fp.getFunct3(ba) == bitarray("000"):
            width = "b"
        elif fp.getFunct3(ba) == bitarray("101"):
            width = "h"
        elif fp.getFunct3(ba) == bitarray("110"):
            width = "w"
        elif fp.getFunct3(ba) == bitarray("111"):
            width = "e"

        if (
            fp.getMOP(ba) == bitarray("000")
            or fp.getMOP(ba) == bitarray("010")
            or fp.getMOP(ba) == bitarray("011")
        ) and width != "e":
            sign = "u"

        if fp.getVM(ba) == bitarray(0):
            vm = "v0.t"

        if fp.getMOP(ba) == bitarray("000") or fp.getMOP(ba) == bitarray("100"):
            data = fp.parseVL(ba)
            if data["nf"] != "seg1":
                nf = data["nf"]
            if fp.getRS2(ba) == bitarray("10000"):
                umop = "ff"
            name = "vl" + nf + width + sign + umop + ".v"
            return RVInstruction(
                rv_format="VL",
                rv_src_registers=[data["rs1"]],
                rv_dest_registers=[data["vd"]],
                rv_mask=vm,
                rv_name=name,
                rv_size=32,
                rv_binary=ba,
            )
        elif fp.getMOP(ba) == bitarray("010") or fp.getMOP(ba) == bitarray("110"):
            data = fp.parseVLS(ba)
            if data["nf"] != "seg1":
                nf = data["nf"]
            name = "vls" + nf + width + sign + ".v"
            return RVInstruction(
                rv_format="VLS",
                rv_src_registers=[data["rs1"], data["rs2"]],
                rv_dest_registers=[data["vd"]],
                rv_mask=vm,
                rv_name=name,
                rv_size=32,
                rv_binary=ba,
            )
        elif fp.getMOP(ba) == bitarray("011") or fp.getMOP(ba) == bitarray("111"):
            data = fp.parseVLX(ba)
            if data["nf"] != "seg1":
                nf = data["nf"]
            name = "vlx" + nf + width + sign + ".v"
            return RVInstruction(
                rv_format="VLX",
                rv_src_registers=[data["rs1"], data["vs2"]],
                rv_dest_registers=[data["vd"]],
                rv_mask=vm,
                rv_name=name,
                rv_size=32,
                rv_binary=ba,
            )
        else:
            # TODO add error message?
            pass

    @staticmethod
    def STORE_FP(ba):
        """Creates Vector Store Instructions"""
        nf = ""
        width = ""
        umop = ""
        vm = ""

        if (
            fp.getFunct3(ba) == bitarray("001")
            or fp.getFunct3(ba) == bitarray("010")
            or fp.getFunct3(ba) == bitarray("011")
            or fp.getFunct3(ba) == bitarray("100")
        ):
            width = ""  # TODO figure out how to display these
        elif fp.getFunct3(ba) == bitarray("000"):
            width = "b"
        elif fp.getFunct3(ba) == bitarray("101"):
            width = "h"
        elif fp.getFunct3(ba) == bitarray("110"):
            width = "w"
        elif fp.getFunct3(ba) == bitarray("111"):
            width = "e"

        if fp.getVM(ba) == bitarray(0):
            vm = "v0.t"

        if fp.getMOP(ba) == bitarray("000"):
            data = fp.parseVS(ba)
            if data["nf"] != "seg1":
                nf = data["nf"]
            name = "vs" + str(nf) + width + ".v"
            return RVInstruction(
                rv_format="VS",
                rv_src_registers=[data["rs1"]],
                rv_dest_registers=[data["vs3"]],
                rv_mask=vm,
                rv_name=name,
                rv_size=32,
                rv_binary=ba,
            )
        elif fp.getMOP(ba) == bitarray("010"):
            data = fp.parseVSS(ba)
            if data["nf"] != "seg1":
                nf = data["nf"]
            name = "vss" + nf + width + ".v"
            return RVInstruction(
                rv_format="VSS",
                rv_src_registers=[data["rs1"], data["rs2"]],
                rv_dest_registers=[data["vs3"]],
                rv_mask=vm,
                rv_name=name,
                rv_size=32,
                rv_binary=ba,
            )
        elif fp.getMOP(ba) == bitarray("011"):
            data = fp.parseVSX(ba)
            if data["nf"] != "seg1":
                nf = data["nf"]
            name = "vsx" + nf + width + ".v"
            return RVInstruction(
                rv_format="VSX",
                rv_src_registers=[data["rs1"], data["vs2"]],
                rv_dest_registers=[data["vs3"]],
                rv_mask=vm,
                rv_name=name,
                rv_size=32,
                rv_binary=ba,
            )
        elif fp.getMOP(ba) == bitarray("111"):
            data = fp.parseVSX(ba)
            if data["nf"] != "seg1":
                nf = data["nf"]
            name = "vsux" + nf + width + ".v"
            return RVInstruction(
                rv_format="VSX",
                rv_src_registers=[data["rs1"], data["vs2"]],
                rv_dest_registers=[data["vs3"]],
                rv_mask=vm,
                rv_name=name,
                rv_size=32,
                rv_binary=ba,
            )
        else:
            # TODO add error message?
            pass

    @staticmethod
    def AMO(ba):
        """Creates Atomic Memory Operation Instructions"""
        data = fp.parseVAMO(ba)

        return RVInstruction(
            rv_format="VAMO",
            rv_src_registers=[data["rs1"], data["vs2"]],
            rv_dest_registers=[data["vd"]],
            rv_size=32,
            rv_binary=ba,
        )

    @staticmethod
    def OP_V(ba):
        """Creates OP-V Instructions"""

        # TODO add data = whichever parser for this one

        f3 = data["funct3"]
        f6 = data["funct6"]
        name = ""

        if f3 == bitarray("000") or f3 == bitarray("011") or f3 == bitarray("100"):
            # OPIVV, OPIVI, OPIVX
            if f6 == bitarray("000000"):
                name = "vadd"
            elif f6 == bitarray("000010"):
                name = "vsub"
            elif f6 == bitarray(""):
                name = "ADD NAME"
            else:
                pass
        elif f3 == bitarray("010") or f3 == bitarray("110"):
            # OPMVV, OPMVX
            if f6 == bitarray("000000"):
                name = "vredsum"
            elif f6 == bitarray("000001"):
                name = "vredand"
            elif f6 == bitarray("000010"):
                name = "vredor"
            elif f6 == bitarray(""):
                name = "ADD NAME"
            else:
                pass
        elif f3 == bitarray("001") or f3 == bitarray("101"):
            # OPFVV, OPFVF
            if f6 == bitarray("000000"):
                name = "vfadd"
            elif f6 == bitarray("000001"):
                name = "vfredsum"
            elif f6 == bitarray("000010"):
                name = "vfsub"
            elif f6 == bitarray(""):
                name = "ADD NAME"
            else:
                pass
        else:
            pass

        if (
            fp.getFunct3(ba) == "000"
        ):  # TODO there's a compiler error at this line...por que?
            data = fp.parseOPIVV(ba)
            return RVInstruction(
                rv_format="OPIVV",
                rv_src_registers=[data["vs1"], data["vs2"]],
                rv_dest_registers=[data["vd"]],
                rv_mask=[data["vm"]],
                rv_name=name,
                rv_size=32,
                rv_binary=ba,
            )
        elif fp.getFunct3(ba) == "001" or fp.getFunct3(ba) == "010":
            data = fp.parseOPFVV(ba)
            return RVInstruction(
                rv_format="OPFVV",
                rv_src_registers=[data["vs1"], data["vs2"]],
                rv_dest_registers=[data["vd"]],  # TODO just vd or vd/rd?
                rv_mask=[data["vm"]],
                rv_name=name,
                rv_size=32,
                rv_binary=ba,
            )
        elif fp.getFunct3(ba) == "011":
            data = fp.parseOPIVI(ba)
            return RVInstruction(
                rv_format="OPIVI",
                rv_src_registers=[data["vs2"]],
                rv_dest_registers=[data["vd"]],
                rv_immediates=[data["simm5"]],
                rv_mask=[data["vm"]],
                rv_name=name,
                rv_size=32,
                rv_binary=ba,
            )
        elif fp.getFunct3(ba) == "100" or fp.getFunct3(ba) == "101":
            data = fp.parseOPIVX(ba)
            return RVInstruction(
                rv_format="OPIVX",
                rv_src_registers=[data["rs1"], data["vs2"]],
                rv_dest_registers=[data["vd"]],
                rv_mask=[data["vm"]],
                rv_name=name,
                rv_size=32,
                rv_binary=ba,
            )
        elif fp.getFunct3(ba) == "110":
            data = fp.parseOPMVX(ba)
            return RVInstruction(
                rv_format="OPMVX",
                rv_src_registers=[data["rs1"], data["vs2"]],
                rv_dest_registers=[data["vd"]],  # TODO just vd or vd/rd?
                rv_mask=[data["vm"]],
                rv_name=name,
                rv_size=32,
                rv_binary=ba,
            )
        elif fp.getFunct3(ba) == "111" and fp.getVSetMSB(ba) == "0":
            data = fp.parseVSetVLI(ba)
            return RVInstruction(
                rv_format="vsetvli",
                rv_src_registers=[data["rs1"]],
                rv_dest_registers=[data["rd"]],
                rv_immediates=[data["zimm"]],
                rv_name=name,
                rv_size=32,
                rv_binary=ba,
            )
        elif fp.getFunct3(ba) == "111" and fp.getVSetMSB(ba) == "1":
            data = fp.parseVSetVL(ba)
            return RVInstruction(
                rv_format="vsetvl",
                rv_src_registers=[data["rs1"], data["rs2"]],
                rv_dest_registers=[data["rd"]],
                rv_name=name,
                rv_size=32,
                rv_binary=ba,
            )

    # dictionary of opcodes --> functions(bitarray) --> RVInstruction
    instructionTable = {
        frozenbitarray("0000111"): LOAD_FP.__func__,
        frozenbitarray("0100111"): STORE_FP.__func__,
        frozenbitarray("0101111"): AMO.__func__,
        frozenbitarray("1010111"): OP_V.__func__,
    }

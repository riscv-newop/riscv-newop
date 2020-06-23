# TODO add rv_name for all the returns
# TODO add all the funct6's listed in the spec

from bitarray import bitarray, frozenbitarray

from . import RVFormatParser as fp
from . import RVInstruction


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
            width = ""  # TODO figure out how to display these
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
        data_width = data["width"]
        data_amoop = data["amoop"]
        src_registers = []
        dest_registers = []
        vm = ""

        if data_width == bitarray("010"):
            width = ".w"
        elif data_width == bitarray("011"):
            width = ".d"
        elif data_width == bitarray("100"):
            width = ".q"
        elif data_width == bitarray("110"):
            width = "w.v"
        elif data_width == bitarray("111"):
            width = "e.v"

        if data_amoop == bitarray("00000"):
            amoop = "vamoadd"
        elif data_amoop == bitarray("00001"):
            amoop = "vamoswap"
        elif data_amoop == bitarray("00100"):
            amoop = "vamoxor"
        elif data_amoop == bitarray("01000"):
            amoop = "vamoor"
        elif data_amoop == bitarray("01100"):
            amoop = "vamoand"
        elif data_amoop == bitarray("10000"):
            amoop = "vamomin"
        elif data_amoop == bitarray("10100"):
            amoop = "vamomax"
        elif data_amoop == bitarray("11000"):
            amoop = "vamominu"
        elif data_amoop == bitarray("11100"):
            amoop = "vamomaxu"

        name = amoop + width

        if data["vm"] == bitarray(0):
            vm = "v0.t"

        if bitarray([ba[-27]]) == bitarray("0"):
            src_registers = [data["rs1"], data["vs2"], data["vd"]]  # vd represents vs3
            dest_registers = ["x0"]
        elif bitarray([ba[-27]]) == bitarray("1"):
            src_registers = [
                data["rs1"],
                data["vs2"],
                data["vd"],
            ]  # TODO is it correct to write vd as a src?
            dest_registers = [data["vd"]]

        return RVInstruction(
            rv_format="VAMO",
            rv_src_registers=src_registers,
            rv_dest_registers=dest_registers,
            rv_mask=vm,
            rv_name=name,
            rv_size=32,
            rv_binary=ba,
        )

    @staticmethod
    def OP_V(ba):
        """Creates OP-V Instructions"""
        f3 = fp.getFunct3(ba)
        f6 = fp.getFunct6(ba)
        vm = ""

        if f3 == bitarray("000") or f3 == bitarray("011") or f3 == bitarray("100"):
            # OPIVV, OPIVI, OPIVX
            if f6 == bitarray("000000"):
                vop = "vadd"
            elif f6 == bitarray("000010"):
                vop = "vsub"
            elif f6 == bitarray("000011"):
                vop = "vrsub"
            elif f6 == bitarray("010111"):
                vop = "vmerge"
            elif f6 == bitarray("011000"):
                vop = "vmseq"
            else:
                pass

            if (
                f6 == bitarray("000000")
                or f6 == bitarray("000001")
                or f6 == bitarray("000010")
                or f6 == bitarray("000011")
                or f6 == bitarray("000100")
                or f6 == bitarray("000101")
                or f6 == bitarray("000110")
                or f6 == bitarray("000111")
                or f6 == bitarray("001000")
                or f6 == bitarray("001001")
                or f6 == bitarray("001010")
                or f6 == bitarray("001011")
                or f6 == bitarray("001100")
                or f6 == bitarray("001101")
                or f6 == bitarray("001110")
                or f6 == bitarray("001111")
            ):
                # TODO swap order of source registers
                if f3 == bitarray("000"):
                    source = ".vv"
                elif f3 == bitarray("100"):
                    source = ".vx"
                elif f3 == bitarray("011"):
                    source = ".vi"
                if fp.getVM(ba) == bitarray(0):
                    vm = "v0.t"
            elif (
                f6 == bitarray("010000")
                or f6 == bitarray("010001")
                or f6 == bitarray("010010")
                or f6 == bitarray("010011")
                or f6 == bitarray("010100")
                or f6 == bitarray("010101")
                or f6 == bitarray("010110")
                or f6 == bitarray("010111")
            ):
                # TODO swap order of source registers
                if f3 == bitarray("000"):
                    source = ".vvm"
                elif f3 == bitarray("100"):
                    source = ".vxm"
                elif f3 == bitarray("011"):
                    source = ".vim"
                vm = "v0"
            elif (
                f6 == bitarray("011000")
                or f6 == bitarray("011001")
                or f6 == bitarray("011010")
                or f6 == bitarray("011011")
                or f6 == bitarray("011100")
                or f6 == bitarray("011101")
                or f6 == bitarray("011110")
                or f6 == bitarray("011111")
            ):
                # TODO swap order of source registers
                if f3 == bitarray("000"):
                    source = ".vv"
                elif f3 == bitarray("100"):
                    source = ".vx"
                elif f3 == bitarray("011"):
                    source = ".vi"
                if fp.getVM(ba) == bitarray(0):
                    vm = "v0.t"
        elif f3 == bitarray("010") or f3 == bitarray("110"):
            # OPMVV, OPMVX
            if f6 == bitarray("000000"):
                vop = "vredsum"
            elif f6 == bitarray("000001"):
                vop = "vredand"
            elif f6 == bitarray("000010"):
                vop = "vredor"
            elif f6 == bitarray("001110"):
                vop = "vslide1up"
            elif f6 == bitarray("010111"):
                vop = "vcompress"
            elif f6 == bitarray("011000"):
                vop = "vmandnot"
            else:
                pass

            if (
                f6 == bitarray("000000")
                or f6 == bitarray("000001")
                or f6 == bitarray("000010")
                or f6 == bitarray("000011")
                or f6 == bitarray("000100")
                or f6 == bitarray("000101")
                or f6 == bitarray("000110")
                or f6 == bitarray("000111")
                or f6 == bitarray("001000")
                or f6 == bitarray("001001")
                or f6 == bitarray("001010")
                or f6 == bitarray("001011")
                or f6 == bitarray("001100")
                or f6 == bitarray("001101")
                or f6 == bitarray("001110")
                or f6 == bitarray("001111")
            ):
                # TODO swap order of source registers
                if "red" in vop:
                    source = ".vs"
                else:
                    if f3 == bitarray("010"):
                        source = ".vv"
                    elif f3 == bitarray("110"):
                        source = ".vx"
                if fp.getVM(ba) == bitarray(0):
                    vm = "v0.t"
            elif (
                f6 == bitarray("010000")
                or f6 == bitarray("010001")
                or f6 == bitarray("010010")
                or f6 == bitarray("010011")
                or f6 == bitarray("010100")
                or f6 == bitarray("010101")
                or f6 == bitarray("010110")
                or f6 == bitarray("010111")
            ):
                # TODO swap order of source registers
                source = ".vm"
            elif (
                f6 == bitarray("011000")
                or f6 == bitarray("011001")
                or f6 == bitarray("011010")
                or f6 == bitarray("011011")
                or f6 == bitarray("011100")
                or f6 == bitarray("011101")
                or f6 == bitarray("011110")
                or f6 == bitarray("011111")
            ):
                # TODO swap order of source registers
                source = ".mm"
        elif f3 == bitarray("001") or f3 == bitarray("101"):
            # OPFVV, OPFVF
            if f6 == bitarray("000000"):
                vop = "vfadd"
            elif f6 == bitarray("000001"):
                vop = "vfredsum"
            elif f6 == bitarray("000010"):
                vop = "vfsub"
            elif f6 == bitarray("010111"):
                vop = "vfmerge"
            elif f6 == bitarray("011000"):
                vop = "vmfeq"
            else:
                pass

            if (
                f6 == bitarray("000000")
                or f6 == bitarray("000001")
                or f6 == bitarray("000010")
                or f6 == bitarray("000011")
                or f6 == bitarray("000100")
                or f6 == bitarray("000101")
                or f6 == bitarray("000110")
                or f6 == bitarray("000111")
                or f6 == bitarray("001000")
                or f6 == bitarray("001001")
                or f6 == bitarray("001010")
                or f6 == bitarray("001011")
                or f6 == bitarray("001100")
                or f6 == bitarray("001101")
                or f6 == bitarray("001110")
                or f6 == bitarray("001111")
            ):
                # TODO swap order of source registers
                if "red" in vop:
                    source = ".vs"
                else:
                    if f3 == bitarray("001"):
                        source = ".vv"
                    elif f3 == bitarray("101"):
                        source = ".vf"
                if fp.getVM(ba) == bitarray(0):
                    vm = "v0.t"
            elif (
                f6 == bitarray("010000")
                or f6 == bitarray("010001")
                or f6 == bitarray("010010")
                or f6 == bitarray("010011")
                or f6 == bitarray("010100")
                or f6 == bitarray("010101")
                or f6 == bitarray("010110")
                or f6 == bitarray("010111")
            ):
                # TODO swap order of source registers
                source = ".vfm"
                vm = "v0"
            elif (
                f6 == bitarray("011000")
                or f6 == bitarray("011001")
                or f6 == bitarray("011010")
                or f6 == bitarray("011011")
                or f6 == bitarray("011100")
                or f6 == bitarray("011101")
                or f6 == bitarray("011110")
                or f6 == bitarray("011111")
            ):
                # TODO swap order of source registers
                if f3 == bitarray("001"):
                    source = ".vv"
                elif f3 == bitarray("101"):
                    source = ".vf"
                if fp.getVM(ba) == bitarray(0):
                    vm = "v0.t"
        else:
            pass

        name = vop + source

        if fp.getFunct3(ba) == bitarray("000"):
            data = fp.parseOPIVV(ba)
            return RVInstruction(
                rv_format="OPIVV",
                rv_src_registers=[data["vs1"], data["vs2"]],
                rv_dest_registers=[data["vd"]],
                rv_mask=vm,
                rv_name=name,
                rv_size=32,
                rv_binary=ba,
            )
        elif fp.getFunct3(ba) == bitarray("001") or fp.getFunct3(ba) == bitarray("010"):
            data = fp.parseOPFVV(ba)
            return RVInstruction(
                rv_format="OPFVV",
                rv_src_registers=[data["vs1"], data["vs2"]],
                rv_dest_registers=[data["vd"]],  # TODO just vd or vd/rd?
                rv_mask=vm,
                rv_name=name,
                rv_size=32,
                rv_binary=ba,
            )
        elif fp.getFunct3(ba) == bitarray("011"):
            data = fp.parseOPIVI(ba)
            return RVInstruction(
                rv_format="OPIVI",
                rv_src_registers=[data["vs2"]],
                rv_dest_registers=[data["vd"]],
                rv_immediates=[data["simm5"]],
                rv_mask=vm,
                rv_name=name,
                rv_size=32,
                rv_binary=ba,
            )
        elif fp.getFunct3(ba) == bitarray("100") or fp.getFunct3(ba) == bitarray("101"):
            data = fp.parseOPIVX(ba)
            return RVInstruction(
                rv_format="OPIVX",
                rv_src_registers=[data["rs1"], data["vs2"]],
                rv_dest_registers=[data["vd"]],
                rv_mask=vm,
                rv_name=name,
                rv_size=32,
                rv_binary=ba,
            )
        elif fp.getFunct3(ba) == bitarray("110"):
            data = fp.parseOPMVX(ba)
            return RVInstruction(
                rv_format="OPMVX",
                rv_src_registers=[data["rs1"], data["vs2"]],
                rv_dest_registers=[data["vd"]],  # TODO just vd or vd/rd?
                rv_mask=vm,
                rv_name=name,
                rv_size=32,
                rv_binary=ba,
            )
        elif fp.getFunct3(ba) == bitarray("111") and fp.getVSetMSB(ba) == bitarray("0"):
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
        elif fp.getFunct3(ba) == bitarray("111") and fp.getVSetMSB(ba) == bitarray("1"):
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

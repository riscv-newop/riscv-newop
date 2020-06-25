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
        s1 = fp.getRS1(ba)
        vs2 = fp.getRS2(ba)
        src_register_swap = False
        vm = ""

        if f3 == bitarray("000") or f3 == bitarray("011") or f3 == bitarray("100"):
            # OPIVV, OPIVI, OPIVX
            if f6 == bitarray("000000"):
                vop = "vadd"
            elif f6 == bitarray("000001"):
                # reserved
                pass
            elif f6 == bitarray("000010"):
                vop = "vsub"
            elif f6 == bitarray("000011"):
                vop = "vrsub"
            elif f6 == bitarray("000100"):
                vop = "vminu"
            elif f6 == bitarray("000101"):
                vop = "vmin"
            elif f6 == bitarray("000110"):
                vop = "vmaxu"
            elif f6 == bitarray("000111"):
                vop = "vmax"
            elif f6 == bitarray("001000"):
                # reserved
                pass
            elif f6 == bitarray("001001"):
                vop = "vand"
            elif f6 == bitarray("001010"):
                vop = "vor"
            elif f6 == bitarray("001011"):
                vop = "vxor"
            elif f6 == bitarray("001100"):
                vop = "vrgather"
            elif f6 == bitarray("001101"):
                # reserved
                pass
            elif f6 == bitarray("001110"):
                vop = "vslideup"
            elif f6 == bitarray("001111"):
                vop = "vslidedown"
            elif f6 == bitarray("010000"):
                vop = "vadc"
            elif f6 == bitarray("010001"):
                vop = "vmadc"
            elif f6 == bitarray("010010"):
                vop = "vsbc"
            elif f6 == bitarray("010011"):
                vop = "vmsbc"
            elif f6 == bitarray("010100"):
                # reserved
                pass
            elif f6 == bitarray("010101"):
                # reserved
                pass
            elif f6 == bitarray("010110"):
                # reserved
                pass
            elif f6 == bitarray("010111"):
                # TODO vmerge/vmv
                vop = "vmerge"
            elif f6 == bitarray("011000"):
                vop = "vmseq"
            elif f6 == bitarray("011001"):
                vop = "vmsne"
            elif f6 == bitarray("011010"):
                vop = "vmsltu"
            elif f6 == bitarray("011011"):
                vop = "vmslt"
            elif f6 == bitarray("011100"):
                vop = "vmsleu"
            elif f6 == bitarray("011101"):
                vop = "vmsle"
            elif f6 == bitarray("011110"):
                vop = "vmsgtu"
            elif f6 == bitarray("011111"):
                vop = "vmsgt"
            elif f6 == bitarray("100000"):
                vop = "vsaddu"
            elif f6 == bitarray("100001"):
                vop = "vsadd"
            elif f6 == bitarray("100010"):
                vop = "vssubu"
            elif f6 == bitarray("100011"):
                vop = "vssub"
            elif f6 == bitarray("100100"):
                vop = "vaadd"
            elif f6 == bitarray("100101"):
                vop = "vsll"
            elif f6 == bitarray("100110"):
                vop = "vasub"
            elif f6 == bitarray("100111"):
                vop = "vsmul"
            elif f6 == bitarray("101000"):
                vop = "vsrl"
            elif f6 == bitarray("101001"):
                vop = "vsra"
            elif f6 == bitarray("101010"):
                vop = "vssrl"
            elif f6 == bitarray("101011"):
                vop = "vssra"
            elif f6 == bitarray("101100"):
                vop = "vnsrl"
            elif f6 == bitarray("101101"):
                vop = "vnsra"
            elif f6 == bitarray("101110"):
                vop = "vnclipu"
            elif f6 == bitarray("101111"):
                vop = "vnclip"
            elif f6 == bitarray("110000"):
                vop = "vwredsumu"
            elif f6 == bitarray("110001"):
                # reserved
                pass
            elif f6 == bitarray("110010"):
                # reserved
                pass
            elif f6 == bitarray("110011"):
                # reserved
                pass
            elif f6 == bitarray("110100"):
                # reserved
                pass
            elif f6 == bitarray("110101"):
                # reserved
                pass
            elif f6 == bitarray("110110"):
                # reserved
                pass
            elif f6 == bitarray("110111"):
                # reserved
                pass
            elif f6 == bitarray("111000"):
                vop = "vdotu"
            elif f6 == bitarray("111001"):
                vop = "vdot"
            elif f6 == bitarray("111010"):
                # reserved
                pass
            elif f6 == bitarray("111011"):
                # reserved
                pass
            elif f6 == bitarray("111100"):
                vop = "vwsmaccu"
            elif f6 == bitarray("111101"):
                vop = "vwsmacc"
            elif f6 == bitarray("111110"):
                vop = "vwsmaccus"
            elif f6 == bitarray("111111"):
                vop = "vwsmaccsu"

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
                src_register_swap = True
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
                src_register_swap = True
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
                src_register_swap = True
                if f3 == bitarray("000"):
                    source = ".vv"
                elif f3 == bitarray("100"):
                    source = ".vx"
                elif f3 == bitarray("011"):
                    source = ".vi"
                if fp.getVM(ba) == bitarray(0):
                    vm = "v0.t"
            elif (
                f6 == bitarray("100000")
                or f6 == bitarray("100001")
                or f6 == bitarray("100010")
                or f6 == bitarray("100011")
                or f6 == bitarray("100100")
                or f6 == bitarray("100101")
                or f6 == bitarray("100110")
                or f6 == bitarray("100111")
                or f6 == bitarray("101000")
                or f6 == bitarray("101001")
                or f6 == bitarray("101010")
                or f6 == bitarray("101011")
                or f6 == bitarray("101100")
                or f6 == bitarray("101101")
                or f6 == bitarray("101110")
                or f6 == bitarray("101111")
            ):
                src_register_swap = True
                if f3 == bitarray("000"):
                    source = ".vv"
                elif f3 == bitarray("100"):
                    source = ".vx"
                elif f3 == bitarray("011"):
                    source = ".vi"
                if fp.getVM(ba) == bitarray(0):
                    vm = "v0.t"
            elif (
                f6 == bitarray("110000")
                or f6 == bitarray("110001")
                or f6 == bitarray("110010")
                or f6 == bitarray("110011")
                or f6 == bitarray("110100")
                or f6 == bitarray("110101")
                or f6 == bitarray("110110")
                or f6 == bitarray("110111")
                or f6 == bitarray("111000")
                or f6 == bitarray("111001")
                or f6 == bitarray("111010")
                or f6 == bitarray("111011")
            ):
                src_register_swap = True
                if "red" in vop:
                    source = ".vs"
                else:
                    if f3 == bitarray("000"):
                        source = ".vv"
                    elif f3 == bitarray("100"):
                        source = ".vx"
                    elif f3 == bitarray("011"):
                        source = ".vi"
                if fp.getVM(ba) == bitarray(0):
                    vm = "v0.t"
            elif (
                f6 == bitarray("111100")
                or f6 == bitarray("111101")
                or f6 == bitarray("111110")
                or f6 == bitarray("111111")
            ):
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
            elif f6 == bitarray("000011"):
                vop = "vredxor"
            elif f6 == bitarray("000100"):
                vop = "vredminu"
            elif f6 == bitarray("000101"):
                vop = "vredmin"
            elif f6 == bitarray("000110"):
                vop = "vredmaxu"
            elif f6 == bitarray("000111"):
                vop = "vredmax"
            elif f6 == bitarray("001000"):
                # reserved
                pass
            elif f6 == bitarray("001001"):
                # reserved
                pass
            elif f6 == bitarray("001010"):
                # reserved
                pass
            elif f6 == bitarray("001011"):
                # reserved
                pass
            elif f6 == bitarray("001100"):
                # reserved
                pass
            elif f6 == bitarray("001101"):
                # reserved
                pass
            elif f6 == bitarray("001110"):
                vop = "vslide1up"
            elif f6 == bitarray("001111"):
                vop = "vslide1down"
            elif f6 == bitarray("010000"):
                if f3 == bitarray("010"):
                    if s1 == bitarray(00000):
                        vop = "vmv.x.s"
                    elif s1 == bitarray("10000"):
                        vop = "vpopc"
                    elif s1 == bitarray("10001"):
                        vop = "vfirst"
                elif f3 == bitarray("110"):
                    if vs2 == bitarray("00000"):
                        vop = "vmv.s.x"
            elif f6 == bitarray("010001"):
                # reserved
                pass
            elif f6 == bitarray("010010"):
                # reserved
                pass
            elif f6 == bitarray("010011"):
                # reserved
                pass
            elif f6 == bitarray("010100"):
                if s1 == bitarray("00001"):
                    vop = "vmsbf"
                elif s1 == bitarray("00010"):
                    vop = "vmsof"
                elif s1 == bitarray("00011"):
                    vop = "vmsif"
                elif s1 == bitarray("10000"):
                    vop = "viota"
                elif s1 == bitarray("10001"):
                    vop = "vid"
            elif f6 == bitarray("010101"):
                # reserved
                pass
            elif f6 == bitarray("010110"):
                # reserved
                pass
            elif f6 == bitarray("010111"):
                vop = "vcompress"
            elif f6 == bitarray("011000"):
                vop = "vmandnot"
            elif f6 == bitarray("011001"):
                vop = "vmand"
            elif f6 == bitarray("011010"):
                vop = "vmor"
            elif f6 == bitarray("011011"):
                vop = "vmxor"
            elif f6 == bitarray("011100"):
                vop = "vmornot"
            elif f6 == bitarray("011101"):
                vop = "vmnand"
            elif f6 == bitarray("011110"):
                vop = "vmnor"
            elif f6 == bitarray("011111"):
                vop = "vmxnor"
            elif f6 == bitarray("100000"):
                vop = "vdivu"
            elif f6 == bitarray("100001"):
                vop = "vdiv"
            elif f6 == bitarray("100010"):
                vop = "vremu"
            elif f6 == bitarray("100011"):
                vop = "vrem"
            elif f6 == bitarray("100100"):
                vop = "vmulhu"
            elif f6 == bitarray("100101"):
                vop = "vmul"
            elif f6 == bitarray("100110"):
                vop = "vmulhsu"
            elif f6 == bitarray("100111"):
                vop = "vsmul"
            elif f6 == bitarray("101000"):
                # reserved
                pass
            elif f6 == bitarray("101001"):
                vop = "vmadd"
            elif f6 == bitarray("101010"):
                # reserved
                pass
            elif f6 == bitarray("101011"):
                vop = "vnmsub"
            elif f6 == bitarray("101100"):
                # reserved
                pass
            elif f6 == bitarray("101101"):
                vop = "vmacc"
            elif f6 == bitarray("101110"):
                # reserved
                pass
            elif f6 == bitarray("101111"):
                vop = "vnmsac"
            elif f6 == bitarray("110000"):
                vop = "vwaddu"
            elif f6 == bitarray("110001"):
                vop = "vwadd"
            elif f6 == bitarray("110010"):
                vop = "vwsubu"
            elif f6 == bitarray("110011"):
                vop = "vwsub"
            elif f6 == bitarray("110100"):
                vop = "vwaddu.w"
            elif f6 == bitarray("110101"):
                vop = "vwadd.w"
            elif f6 == bitarray("110110"):
                vop = "vwsubu.w"
            elif f6 == bitarray("110111"):
                vop = "vwsub.w"
            elif f6 == bitarray("111000"):
                vop = "vwmulu"
            elif f6 == bitarray("111001"):
                # reserved
                pass
            elif f6 == bitarray("111010"):
                vop = "vwmulsu"
            elif f6 == bitarray("111011"):
                vop = "vwmulu"
            elif f6 == bitarray("111100"):
                vop = "vwmaccu"
            elif f6 == bitarray("111101"):
                vop = "vwmacc"
            elif f6 == bitarray("111110"):
                vop = "vwmaccus"
            elif f6 == bitarray("111111"):
                vop = "vwmaccsu"

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
                src_register_swap = True
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
                src_register_swap = True
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
                src_register_swap = True
                source = ".mm"
            elif (
                f6 == bitarray("100000")
                or f6 == bitarray("100001")
                or f6 == bitarray("100010")
                or f6 == bitarray("100011")
                or f6 == bitarray("100100")
                or f6 == bitarray("100101")
                or f6 == bitarray("100110")
                or f6 == bitarray("100111")
            ):
                src_register_swap = True
                if f3 == bitarray("010"):
                    source = ".vv"
                elif f3 == bitarray("110"):
                    source = ".vx"
                if fp.getVM(ba) == bitarray(0):
                    vm = "v0.t"
            elif (
                f6 == bitarray("101000")
                or f6 == bitarray("101001")
                or f6 == bitarray("101010")
                or f6 == bitarray("101011")
                or f6 == bitarray("101100")
                or f6 == bitarray("101101")
                or f6 == bitarray("101110")
                or f6 == bitarray("101111")
            ):
                if f3 == bitarray("010"):
                    source = ".vv"
                elif f3 == bitarray("110"):
                    source = ".vx"
                if fp.getVM(ba) == bitarray(0):
                    vm = "v0.t"
            elif (
                f6 == bitarray("110000")
                or f6 == bitarray("110001")
                or f6 == bitarray("110010")
                or f6 == bitarray("110011")
                or f6 == bitarray("110100")
                or f6 == bitarray("110101")
                or f6 == bitarray("110110")
                or f6 == bitarray("110111")
                or f6 == bitarray("111000")
                or f6 == bitarray("111001")
                or f6 == bitarray("111010")
                or f6 == bitarray("111011")
            ):
                src_register_swap = True
                if ".w" in vop:
                    if f3 == bitarray("010"):
                        source = "v"
                    elif f3 == bitarray("110"):
                        source = "x"
                else:
                    if f3 == bitarray("010"):
                        source = ".vv"
                    elif f3 == bitarray("110"):
                        source = ".vx"
                if fp.getVM(ba) == bitarray(0):
                    vm = "v0.t"
            elif (
                f6 == bitarray("111100")
                or f6 == bitarray("111101")
                or f6 == bitarray("111110")
                or f6 == bitarray("111111")
            ):
                if f3 == bitarray("010"):
                    source = ".vv"
                elif f3 == bitarray("110"):
                    source = ".vx"
                if fp.getVM(ba) == bitarray(0):
                    vm = "v0.t"
        elif f3 == bitarray("001") or f3 == bitarray("101"):
            # OPFVV, OPFVF
            if f6 == bitarray("000000"):
                vop = "vfadd"
            elif f6 == bitarray("000001"):
                vop = "vfredsum"
            elif f6 == bitarray("000010"):
                vop = "vfsub"
            elif f6 == bitarray("000011"):
                vop = "vfredosum"
            elif f6 == bitarray("000100"):
                vop = "vfmin"
            elif f6 == bitarray("000101"):
                vop = "vfredmin"
            elif f6 == bitarray("000110"):
                vop = "vfmax"
            elif f6 == bitarray("000111"):
                vop = "vfredmax"
            elif f6 == bitarray("001000"):
                vop = "vfsgnj"
            elif f6 == bitarray("001001"):
                vop = "vfsgnjn"
            elif f6 == bitarray("001010"):
                vop = "vfsgnjx"
            elif f6 == bitarray("001011"):
                # reserved
                pass
            elif f6 == bitarray("001100"):
                # reserved
                pass
            elif f6 == bitarray("001101"):
                # reserved
                pass
            elif f6 == bitarray("001110"):
                # reserved
                pass
            elif f6 == bitarray("001111"):
                # reserved
                pass
            elif f6 == bitarray("010000"):
                if f3 == bitarray("001"):
                    if s1 == bitarray("00000"):
                        vop = "vfmv.f.s"
                elif f3 == bitarray("101"):
                    if vs2 == bitarray("00000"):
                        vop = "vfmv.s.f"
            elif f6 == bitarray("010001"):
                # reserved
                pass
            elif f6 == bitarray("010010"):
                # reserved
                pass
            elif f6 == bitarray("010011"):
                # reserved
                pass
            elif f6 == bitarray("010100"):
                # reserved
                pass
            elif f6 == bitarray("010101"):
                # reserved
                pass
            elif f6 == bitarray("010110"):
                # reserved
                pass
            elif f6 == bitarray("010111"):
                # TODO vfmv
                vop = "vfmerge.vf"
            elif f6 == bitarray("011000"):
                vop = "vmfeq"
            elif f6 == bitarray("011001"):
                vop = "vmfle"
            elif f6 == bitarray("011010"):
                # reserved
                pass
            elif f6 == bitarray("011011"):
                vop = "vmflt"
            elif f6 == bitarray("011100"):
                vop = "vmfne"
            elif f6 == bitarray("011101"):
                vop = "vmfgt"
            elif f6 == bitarray("011110"):
                # reserved
                pass
            elif f6 == bitarray("011111"):
                vop = "vmfge"
            elif f6 == bitarray("100000"):
                vop = "vfdiv"
            elif f6 == bitarray("100001"):
                vop = "vfrdiv"
            elif f6 == bitarray("100010"):
                if s1 == bitarray("00000"):
                    vop = "vfcvt.xu.f.v"
                elif s1 == bitarray("00001"):
                    vop = "vfcvt.x.f.v"
                elif s1 == bitarray("00010"):
                    vop = "vfcvt.f.xu.v"
                elif s1 == bitarray("00011"):
                    vop = "vfcvt.f.x.v"
                elif s1 == bitarray("01000"):
                    vop = "vfwcvt.xu.f.v"
                elif s1 == bitarray("01001"):
                    vop = "vfwcvt.x.f.v"
                elif s1 == bitarray("01010"):
                    vop = "vfwcvt.f.xu.v"
                elif s1 == bitarray("01011"):
                    vop = "vfwcvt.f.x.v"
                elif s1 == bitarray("01100"):
                    vop = "vfwcvt.f.f.v"
                elif s1 == bitarray("10000"):
                    vop = "vfncvt.xu.f.v"
                elif s1 == bitarray("10001"):
                    vop = "vfncvt.x.f.v"
                elif s1 == bitarray("10010"):
                    vop = "vfncvt.f.xu.v"
                elif s1 == bitarray("10011"):
                    vop = "vfncvt.f.x.v"
                elif s1 == bitarray("10100"):
                    vop = "vfncvt.f.f.v"
            elif f6 == bitarray("100011"):
                if s1 == bitarray("00000"):
                    vop = "vfsqrt.v"
                elif s1 == bitarray("10000"):
                    vop = "vfclass.v"
            elif f6 == bitarray("100100"):
                vop = "vfmul"
            elif f6 == bitarray("100101"):
                # reserved
                pass
            elif f6 == bitarray("100110"):
                # reserved
                pass
            elif f6 == bitarray("100111"):
                vop = "vfrsub"
            elif f6 == bitarray("101000"):
                vop = "vfmadd"
            elif f6 == bitarray("101001"):
                vop = "vfnmadd"
            elif f6 == bitarray("101010"):
                vop = "vfmsub"
            elif f6 == bitarray("101011"):
                vop = "vfnmsub"
            elif f6 == bitarray("101100"):
                vop = "vfmacc"
            elif f6 == bitarray("101101"):
                vop = "vfnmacc"
            elif f6 == bitarray("101110"):
                vop = "vfmsac"
            elif f6 == bitarray("101111"):
                vop = "vfnmsac"
            elif f6 == bitarray("110000"):
                vop = "vfwadd"
            elif f6 == bitarray("110001"):
                vop = "vfwredsum"
            elif f6 == bitarray("110010"):
                vop = "vfwsub"
            elif f6 == bitarray("110011"):
                vop = "vfwredosum"
            elif f6 == bitarray("110100"):
                vop = "vfwadd.w"
            elif f6 == bitarray("110101"):
                # reserved
                pass
            elif f6 == bitarray("110110"):
                vop = "vfwsub.w"
            elif f6 == bitarray("110111"):
                # reserved
                pass
            elif f6 == bitarray("111000"):
                vop = "vfwmul"
            elif f6 == bitarray("111001"):
                vop = "vfdot"
            elif f6 == bitarray("111010"):
                # reserved
                pass
            elif f6 == bitarray("111011"):
                # reserved
                pass
            elif f6 == bitarray("111100"):
                vop = "vfwmacc"
            elif f6 == bitarray("111101"):
                vop = "vfwnmacc"
            elif f6 == bitarray("111110"):
                vop = "vfwmsac"
            elif f6 == bitarray("111111"):
                vop = "vfwnmsac"

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
                src_register_swap = True
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
                src_register_swap = True
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
                src_register_swap = True
                if f3 == bitarray("001"):
                    source = ".vv"
                elif f3 == bitarray("101"):
                    source = ".vf"
                if fp.getVM(ba) == bitarray(0):
                    vm = "v0.t"
            elif (
                f6 == bitarray("100000")
                or f6 == bitarray("100001")
                or f6 == bitarray("100010")
                or f6 == bitarray("100011")
                or f6 == bitarray("100100")
                or f6 == bitarray("100101")
                or f6 == bitarray("100110")
                or f6 == bitarray("100111")
            ):
                src_register_swap = True
                if f3 == bitarray("001"):
                    source = ".vv"
                elif f3 == bitarray("101"):
                    source = ".vf"
                if fp.getVM(ba) == bitarray(0):
                    vm = "v0.t"
            elif (
                f6 == bitarray("101000")
                or f6 == bitarray("101001")
                or f6 == bitarray("101010")
                or f6 == bitarray("101011")
                or f6 == bitarray("101100")
                or f6 == bitarray("101101")
                or f6 == bitarray("101110")
                or f6 == bitarray("101111")
            ):
                if f3 == bitarray("001"):
                    source = ".vv"
                elif f3 == bitarray("101"):
                    source = ".vf"
                if fp.getVM(ba) == bitarray(0):
                    vm = "v0.t"
            elif (
                f6 == bitarray("110000")
                or f6 == bitarray("110001")
                or f6 == bitarray("110010")
                or f6 == bitarray("110011")
                or f6 == bitarray("110100")
                or f6 == bitarray("110101")
                or f6 == bitarray("110110")
                or f6 == bitarray("110111")
                or f6 == bitarray("111000")
                or f6 == bitarray("111001")
                or f6 == bitarray("111010")
                or f6 == bitarray("111011")
            ):
                src_register_swap = True
                if "red" in vop:
                    source = ".vs"
                elif ".w" in vop:
                    if f3 == bitarray("001"):
                        source = "v"
                    elif f3 == bitarray("101"):
                        source = "f"
                else:
                    if f3 == bitarray("001"):
                        source = ".vv"
                    elif f3 == bitarray("101"):
                        source = ".vf"
                if fp.getVM(ba) == bitarray(0):
                    vm = "v0.t"
            elif (
                f6 == bitarray("111100")
                or f6 == bitarray("111101")
                or f6 == bitarray("111110")
                or f6 == bitarray("111111")
            ):
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
            if src_register_swap == True:
                src_registers = [data["vs2"], data["vs1"]]
            else:
                src_registers = [data["vs1"], data["vs2"]]
            return RVInstruction(
                rv_format="OPIVV",
                rv_src_registers=src_registers,
                rv_dest_registers=[data["vd"]],
                rv_mask=vm,
                rv_name=name,
                rv_size=32,
                rv_binary=ba,
            )
        elif fp.getFunct3(ba) == bitarray("001") or fp.getFunct3(ba) == bitarray("010"):
            data = fp.parseOPFVV(ba)
            if src_register_swap == True:
                src_registers = [data["vs2"], data["vs1"]]
            else:
                src_registers = [data["vs1"], data["vs2"]]
            return RVInstruction(
                rv_format="OPFVV",
                rv_src_registers=src_registers,
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
            if src_register_swap == True:
                src_registers = [data["vs2"], data["rs1"]]
            else:
                src_registers = [data["rs1"], data["vs2"]]
            return RVInstruction(
                rv_format="OPIVX",
                rv_src_registers=src_registers,
                rv_dest_registers=[data["vd"]],
                rv_mask=vm,
                rv_name=name,
                rv_size=32,
                rv_binary=ba,
            )
        elif fp.getFunct3(ba) == bitarray("110"):
            data = fp.parseOPMVX(ba)
            if src_register_swap == True:
                src_registers = [data["vs2"], data["rs1"]]
            else:
                src_registers = [data["rs1"], data["vs2"]]
            return RVInstruction(
                rv_format="OPMVX",
                rv_src_registers=src_registers,
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

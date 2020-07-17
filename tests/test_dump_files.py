import string
import os
from glob import glob
from rvnewop import RV32

import pytest


def isJumpPCRelative(inst_name):
    if inst_name in ["j", "jal", "c.j", "c.jal"]:
        return True
    return False


def isBranchPCRelative(inst_name):
    if inst_name in [
        "beq",
        "bne",
        "blt",
        "bltu",
        "bge",
        "bgeu",
        "beqz",
        "bnez",
        "blez",
        "bgez",
        "bltz",
        "bgtz",
        "bgt",
        "ble",
        "bgtu",
        "bleu",
    ]:
        return True
    return False


def isCompressedBranchPCRelative(inst_name):
    if inst_name in ["c.beqz", "c.bnez"]:
        return True
    return False


class DumpFileReader:
    # TODO get rid of this __init__ and change to a
    # seperate static method since this doesn't require state
    def __init__(self, file_name):
        rv = RV32("32IC")
        if os.path.exists(file_name) == False:
            print("Fatal: Unable to find the file: " + file_name)
        else:
            df_handle = open(file_name, "r")
            lines = df_handle.readlines()
            for line in lines:
                words = line.split()
                # Look for lines with at least 4 space-separated words
                if len(words) > 3:
                    # PC is recorded in the dump file with syntac <PC>:
                    # Strip the : away
                    words[0] = words[0].replace(":", "")

                    # Some false matches such as the line "Disassembly of section .text:"
                    # Remove those by ensuring that the first word is a valid hex value
                    if all(c in string.hexdigits for c in words[0]):
                        inst_pc = words[0]
                        inst_hex = words[1]
                        inst_name = words[2]
                        inst_params = words[3]

                        inst_is_branch_jump = False
                        if isBranchPCRelative(inst_name):
                            inst_is_branch_jump = True
                            branch_dest_param_pos = 2
                        if isCompressedBranchPCRelative(inst_name):
                            inst_is_branch_jump = True
                            branch_dest_param_pos = 1
                        if isJumpPCRelative(inst_name):
                            inst_is_branch_jump = True
                            branch_dest_param_pos = 1
                        if inst_is_branch_jump:
                            inst_params_list = inst_params.split(",")
                            branch_dest = inst_params_list[branch_dest_param_pos]
                            branch_dest = branch_dest.split()[
                                0
                            ]  # split on space and pick first entry which is the actual destination PC
                            # compute PC relative immediate
                            branch_offset = int(branch_dest, 16) - int(inst_pc, 16)
                            inst_params_list[branch_dest_param_pos] = branch_offset
                            inst_params = ",".join(
                                [str(elem) for elem in inst_params_list]
                            )
                        if inst_name in ["lui", "auipc"]:
                            inst_params_temp = inst_params.split(",")
                            inst_params = "{},{}".format(
                                inst_params_temp[0], int(inst_params_temp[1], 16),
                            )

                        if inst_name in ["slli", "srli", "srai"]:
                            print("{} {}".format(inst_name, inst_params))
                            inst_params_temp = inst_params.split(",")
                            inst_params = "{},{},{}".format(
                                inst_params_temp[0],
                                inst_params_temp[1],
                                int(inst_params_temp[2], 16),
                            )
                            print(inst_params)

                        predicted_inst = rv.decodeHex(inst_hex)
                        predicted = str(predicted_inst)

                        if predicted == "unsupported":
                            # do not check unsupported instructions
                            continue

                        inst = "{} {}".format(inst_name, inst_params)

                        # Check predicted instruction is correct
                        assert predicted == inst


def test_dump_file():
    # TODO seperate this into multiple functions
    # to see which ISAs failed
    files = glob(os.path.join("tests", "dump_files/*.dump"))
    for file in files:
        DumpFileReader(file)

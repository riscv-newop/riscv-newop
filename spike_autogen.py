#!/usr/bin/env python

import string
import os
import json
from glob import glob
from pathlib import Path
from bitarray import bitarray

import pytest


class AutoGen:
    def __init__(self, path_name):
        if os.path.exists(path_name) == False:
            print("Fatal: Unable to find the path: " + path_name)
        else:
            json_handle = open("inst.json", "r")

            # TODO get data from json
            insn_dict = json.load(json_handle)
            print(insn_dict)
            for insn in insn_dict:
                print(insn)
            # get name of new insn and save in var insn_name
            insn_name = ["MOD", "name1", "name3"]
            # get "value" of custom-0 (and maybe of funct3 and funct7?)
            insn_match = [0xB, 0x1, 0x2]
            # get "width" of funct7 (or funct6?), funct3, and custon-0, left shift by "start", or with each other
            insn_mask = [0xFE00707F, 0x1, 0x2]
            # get contents of new insn that will go in insns/insn_name.h

            # Write to encoding.h
            encoding_handle = open(os.path.join(path_name, "encoding.h"), "r")
            str_list = encoding_handle.read().split("\n")
            encoding_handle.close()

            # Backup encoding.h
            backup_handle = open(
                os.path.join(path_name, "../backup/encoding_backup.h"), "w"
            )
            print("\n".join(str_list), file=backup_handle)
            backup_handle.close()

            # If Autogen section already exists
            if "// MATCH/MASK AUTOGEN START" in str_list:
                substring1 = "// MATCH/MASK AUTOGEN START"
                substring2 = "// MATCH/MASK AUTOGEN END"
                substring3 = "// DECLARE AUTOGEN START"
                substring4 = "// DECLARE AUTOGEN END"

                # Remove lines between autogen start and autogen end
                for i, s in enumerate(str_list):
                    if substring1 in s:
                        match_start = i
                    if substring2 in s:
                        match_end = i
                del str_list[match_start + 1 : match_end]

                # Add match/mask lines for each insn
                for i in range(len(insn_name)):
                    str_list.insert(
                        match_start + 1 + (i * 2),
                        "#define MATCH_" + insn_name[i] + " " + hex(insn_match[i]),
                    )
                    str_list.insert(
                        match_start + 2 + (i * 2),
                        "#define MASK_" + insn_name[i] + " " + hex(insn_mask[i]),
                    )

                # Remove lines between autogen start and autogen end
                for i, s in enumerate(str_list):
                    if substring3 in s:
                        match_start = i
                    if substring4 in s:
                        match_end = i
                del str_list[match_start + 1 : match_end]

                # Add declare lines for each insn
                for i in range(len(insn_name)):
                    str_list.insert(
                        match_start + 1 + i,
                        "DECLARE_INSN("
                        + insn_name[i]
                        + ", MATCH_"
                        + insn_name[i]
                        + ", MASK_"
                        + insn_name[i]
                        + ")",
                    )

            # If Autogen section does not exist
            else:
                # Find line before Autogen section
                substr = "#define RISCV_ENCODING_H"
                for i, s in enumerate(str_list):
                    if substr in s:
                        match_str = i

                # Add matck/mask lines for each insn
                str_list.insert(match_str + 1, "// MATCH/MASK AUTOGEN START")
                for i in range(len(insn_name)):
                    str_list.insert(
                        match_str + 2 + (i * 2),
                        "#define MATCH_" + insn_name[i] + " " + hex(insn_match[i]),
                    )
                    str_list.insert(
                        match_str + 3 + (i * 2),
                        "#define MASK_" + insn_name[i] + " " + hex(insn_mask[i]),
                    )
                str_list.insert(match_str + 4 + (i * 2), "// MATCH/MASK AUTOGEN END")

                # Find line before Autogen section
                substr = "#ifdef DECLARE_INSN"
                for i, s in enumerate(str_list):
                    if substr in s:
                        match_str = i

                # Add declare lines for each insn
                str_list.insert(match_str + 1, "// DECLARE AUTOGEN START")
                for i in range(len(insn_name)):
                    str_list.insert(
                        match_str + 2 + i,
                        "DECLARE_INSN("
                        + insn_name[i]
                        + ", MATCH_"
                        + insn_name[i]
                        + ", MASK_"
                        + insn_name[i]
                        + ")",
                    )
                str_list.insert(match_str + 3 + i, "// DECLARE AUTOGEN END")

            # Write str_list to encoding.h
            encoding_handle = open(os.path.join(path_name, "encoding.h"), "w")
            print("\n".join(str_list), file=encoding_handle)

            # Write to riscv.mk.in
            # TODO needs to be able to determine the extension of the insn
            make_handle = open(os.path.join(path_name, "riscv.mk.in"), "r+")
            str_list = make_handle.read().split("\n")
            make_handle.close()

            # Backup riscv.mk.in
            backup_handle = open(
                os.path.join(path_name, "../backup/riscv_backup.mk.in"), "w"
            )
            print("\n".join(str_list), file=backup_handle)
            backup_handle.close()

            # If Autogen section exists
            if "# AUTOGEN START" in str_list:
                substring1 = "# AUTOGEN START"
                substring2 = "# AUTOGEN END"

                # Remove lines between Autogen start and end
                for i, s in enumerate(str_list):
                    if substring1 in s:
                        match_start = i
                    if substring2 in s:
                        match_end = i
                del str_list[match_start + 1 : match_end]

                # Add lines for each insn
                for i in range(len(insn_name)):
                    str_list.insert(
                        match_start + 1 + i,
                        "\t" + insn_name[i] + " \\",
                    )

            # If Autogen section does not exist
            else:
                # Find line before Autogen section
                substr = "riscv_insn_ext_i = \\"
                for i, s in enumerate(str_list):
                    if substr in s:
                        match_str = i

                # Add lines for each insn
                str_list.insert(match_str + 1, "# AUTOGEN START")
                for i in range(len(insn_name)):
                    str_list.insert(
                        match_str + 2 + i,
                        "\t" + insn_name[i] + " \\",
                    )
                str_list.insert(match_str + 3 + i, "# AUTOGEN END")

            # Write str_list to riscv.mk.in
            make_handle = open(os.path.join(path_name, "riscv.mk.in"), "w")
            print("\n".join(str_list), file=make_handle)

            # Write to files inside insns/
            # Backup existing insns files with same insn_name
            for i in insn_name:
                f = Path(path_name, "insns/", i + ".h")
                if f.is_file():
                    i_handle = open(os.path.join(path_name, "insns/" + i + ".h"), "r")
                    str_list = i_handle.read().split("\n")
                    i_handle.close()

                    backup_handle = open(
                        os.path.join(path_name, "../backup/" + i + "_backup.h"), "w"
                    )
                    print("\n".join(str_list), file=backup_handle)
                    backup_handle.close()

            # Create new files inside insns/
            for i in range(len(insn_name)):
                insn_handle = open(
                    os.path.join(path_name, "insns/", insn_name[i] + ".h"), "w+"
                )
                insn_handle.close()

            # Close file handlers
            encoding_handle.close()
            make_handle.close()
            json_handle.close()


def spike_autogen():
    path = "../../RISCV/riscv-isa-sim/riscv/"
    AutoGen(path)


spike_autogen()

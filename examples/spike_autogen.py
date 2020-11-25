#!/usr/bin/env python

import string
import os
import json
from glob import glob
from pathlib import Path
from datetime import datetime
from bitarray import bitarray
import sys
import networkx as nx


def usage():
    print("Program takes three arguments:")
    print("New instructions JSON file")
    print("Path to RISCV SPIKE Installation")
    print("Path to a folder/worksapce")


def addSemantic(g, node_id, node, is_root):
    if node["type"] == "instruction":
        # get instruction
        insn_name = node_id.split(":")[1].split(" ")[1]
        insn_args = node_id.split(":")[1].split(" ")[2].split(",")
        for n_c_id in g.neighbors(node_id):
            n_c = g.nodes[n_c_id]
            if n_c["type"] == "instruction":
                print("child is an instruction")
                addSemantic(g, n_c_id, n_c, False)
            elif n_c["type"] == "register":
                print("child is a register")
            elif n_c["type"] == "constant":
                print("child is a constant")


"""
Why is this chunk of code even here? seems like a repeat of the code below. - Tanvi
class AutoGen:
    def __init__(self, new_insn_json, riscv_path_name, backup_path):
        if os.path.exists(riscv_path_name) == False:
            print("Fatal: Unable to find the path: " + riscv_path_name)
        else:
            json_handle = open(new_insn_json, "r")

            # TODO get data from json
            insn_dict = json.load(json_handle)
            # get name of new insn and save in var insn_name
            # insn_name = ["MOD", "name6", "name7"]
            # get "value" of custom-0 (and maybe of funct3 and funct7?)
            # insn_match = [0xB, 0x1, 0x2]
            # get "width" of funct7 (or funct6?), funct3, and custon-0, left shift by "start", or with each other
            # insn_mask = [0xFE00707F, 0x1, 0x2]
            # get contents of new insn that will go in insns/insn_name.h

            # Write to encoding.h
            encoding_handle = open(os.path.join(riscv_path_name, "encoding.h"), "r")
"""


class AutoGen:
    def __init__(self, new_insn_json, riscv_path_name, backup_path):
        if os.path.exists(new_insn_json) == False:
            print("Fatal: Unable to find the path: " + new_insn_json)
        elif os.path.exists(riscv_path_name) == False:
            print("Fatal: Unable to find the path: " + riscv_path_name)
        else:
            # Make backup directory
            if os.path.exists(backup_path) == False:
                os.mkdir(backup_path)

            # Make backup subdirectory with timestamp
            os.mkdir(backup_path + datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
            backup_path = backup_path + datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

            json_handle = open(new_insn_json, "r")

            # TODO get data from json
            insn_dict = json.load(json_handle)

            """
            # get name of new insn and save in var insn_name
            # insn_name = ["MOD", "name6", "name7"]
            # get "value" of custom-0 (and maybe of funct3 and funct7?)
            # insn_match = [0xB, 0x1, 0x2]
            # get "width" of funct7 (or funct6?), funct3, and custon-0, left shift by "start", or with each other
            # insn_mask = [0xFE00707F, 0x1, 0x2]
            # get contents of new insn that will go in insns/insn_name.h
            """

            # Replace .'s for _'s in insn_name
            # TODO uncomment when checked by Gulur
            # TODO replace all ["instructions"][i]["insn_name"]
            # insn_name = insn_dict["instructions"][i]["insn_name"]
            # if "." in insn_name:
            # insn_name = insn_name.replace(".", "_")

            # Write to encoding.h
            encoding_handle = open(os.path.join(riscv_path_name, "encoding.h"), "r")
            str_list = encoding_handle.read().split("\n")
            encoding_handle.close()

            # Backup encoding.h
            backup_handle = open(os.path.join(backup_path, "encoding_backup.h"), "w")
            print("\n".join(str_list), file=backup_handle)
            backup_handle.close()

            # If Autogen section already exists
            if "// MATCH/MASK AUTOGEN START" in str_list:
                substring1 = "// MATCH/MASK AUTOGEN START"
                substring2 = "// MATCH/MASK AUTOGEN END"
                substring3 = "// DECLARE AUTOGEN START"
                substring4 = "// DECLARE AUTOGEN END"

                # Find Autogen section
                for i, s in enumerate(str_list):
                    if substring1 in s:
                        match_start = i
                    if substring2 in s:
                        match_end = i

                # Remove lines between Autogen start and Autogen end
                del str_list[match_start + 1 : match_end]

                # Add match/mask lines for each insn
                for i in range(len(insn_dict["instructions"])):
                    print(insn_dict["instructions"][i])
                    str_list.insert(
                        match_start + 1 + (i * 2),
                        "#define MATCH_"
                        + insn_dict["instructions"][i]["insn_name"]
                        + " "
                        + insn_dict["instructions"][i]["match"],
                    )
                    str_list.insert(
                        match_start + 2 + (i * 2),
                        "#define MASK_"
                        + insn_dict["instructions"][i]["insn_name"]
                        + " "
                        + insn_dict["instructions"][i]["mask"],
                    )

                # Find Autogen section
                for i, s in enumerate(str_list):
                    if substring3 in s:
                        match_start = i
                    if substring4 in s:
                        match_end = i

                # Remove lines between Autogen start and Autogen end
                del str_list[match_start + 1 : match_end]

                # Add declare lines for each insn
                for i in range(len(insn_dict["instructions"])):
                    str_list.insert(
                        match_start + 1 + i,
                        "DECLARE_INSN("
                        + insn_dict["instructions"][i]["insn_name"]
                        + ", MATCH_"
                        + insn_dict["instructions"][i]["insn_name"]
                        + ", MASK_"
                        + insn_dict["instructions"][i]["insn_name"]
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
                for i in range(len(insn_dict["instructions"])):
                    str_list.insert(
                        match_str + 2 + (i * 2),
                        "#define MATCH_"
                        + insn_dict["instructions"][i]["insn_name"]
                        + " "
                        + insn_dict["instructions"][i]["match"],
                    )
                    str_list.insert(
                        match_str + 3 + (i * 2),
                        "#define MASK_"
                        + insn_dict["instructions"][i]["insn_name"]
                        + " "
                        + insn_dict["instructions"][i]["mask"],
                    )
                str_list.insert(match_str + 4 + (i * 2), "// MATCH/MASK AUTOGEN END")

                # Find line before Autogen section
                substr = "#ifdef DECLARE_INSN"
                for i, s in enumerate(str_list):
                    if substr in s:
                        match_str = i

                # Add declare lines for each insn
                str_list.insert(match_str + 1, "// DECLARE AUTOGEN START")
                for i in range(len(insn_dict["instructions"])):
                    str_list.insert(
                        match_str + 2 + i,
                        "DECLARE_INSN("
                        + insn_dict["instructions"][i]["insn_name"]
                        + ", MATCH_"
                        + insn_dict["instructions"][i]["match"]
                        + ", MASK_"
                        + insn_dict["instructions"][i]["mask"]
                        + ")",
                    )
                str_list.insert(match_str + 3 + i, "// DECLARE AUTOGEN END")

            # Write str_list to encoding.h
            encoding_handle = open(os.path.join(riscv_path_name, "encoding.h"), "w")
            print("\n".join(str_list), file=encoding_handle)

            # Write to riscv.mk.in
            # TODO needs to be able to determine the extension of the insn
            make_handle = open(os.path.join(riscv_path_name, "riscv.mk.in"), "r+")
            str_list = make_handle.read().split("\n")
            make_handle.close()

            # Backup riscv.mk.in
            backup_handle = open(os.path.join(backup_path, "riscv_backup.mk.in"), "w")
            print("\n".join(str_list), file=backup_handle)
            backup_handle.close()

            # Find line before Autogen section
            substring1 = "riscv_insn_ext_i = \\"
            substring2 = "\tadd \\"
            for i, s in enumerate(str_list):
                if substring1 in s:
                    match_start = i
                if substring2 in s:
                    match_end = i

            # Remove lines between Autogen start and end
            del str_list[match_start + 1 : match_end]

            # Add lines for each insn
            for i in range(len(insn_dict["instructions"])):
                str_list.insert(
                    match_start + 1 + i,
                    "\t" + insn_dict["instructions"][i]["insn_name"] + " \\",
                )

            # Write str_list to riscv.mk.in
            make_handle = open(os.path.join(riscv_path_name, "riscv.mk.in"), "w")
            print("\n".join(str_list), file=make_handle)

            # Write to files inside insns/
            # Backup existing insns files with same insn_name
            for i in range(len(insn_dict["instructions"])):
                f = Path(
                    riscv_path_name,
                    "insns/",
                    insn_dict["instructions"][i]["insn_name"] + ".h",
                )
                if f.is_file():
                    file_name = os.path.join(
                        riscv_path_name,
                        "insns/" + insn_dict["instructions"][i]["insn_name"] + ".h",
                    )
                    print("opening " + file_name)
                    i_handle = open(
                        os.path.join(
                            riscv_path_name,
                            "insns/" + insn_dict["instructions"][i]["insn_name"] + ".h",
                        ),
                        "r",
                    )
                    str_list = i_handle.read().split("\n")
                    i_handle.close()

                    backup_handle = open(
                        os.path.join(backup_path, str(i) + "_backup.h"), "w"
                    )
                    print("\n".join(str_list), file=backup_handle)
                    backup_handle.close()

            # Create new files inside insns/
            for i in range(len(insn_dict["instructions"])):
                insn_handle = open(
                    os.path.join(
                        riscv_path_name,
                        "insns/",
                        insn_dict["instructions"][i]["insn_name"] + ".h",
                    ),
                    "w+",
                )
                # create graph object from JSON
                g = nx.readwrite.json_graph.adjacency_graph(
                    insn_dict["instructions"][i]["graph"]
                )

                # get root of g
                root = None
                for n, d in g.in_degree():
                    if d == 0:
                        root = n
                # traverse the graph starting with root and generate semantic function
                subgraph_nodes = [
                    y for x in nx.bfs_edges(g, source=root) for y in x if y is not root
                ]

                execute_func_str = addSemantic(g, root, g.nodes[root], True)

                insn_handle.close()

            # Close file handlers
            encoding_handle.close()
            make_handle.close()
            json_handle.close()


if len(sys.argv) < 4:
    usage()
    sys.exit()

new_insn_json = sys.argv[1]
path = sys.argv[2]
backup = sys.argv[3]

AutoGen(new_insn_json, path, backup)

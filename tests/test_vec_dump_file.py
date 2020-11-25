#!/usr/bin/env python

import string
import os
from glob import glob
from rvnewop import RV32
from bitarray import bitarray

import pytest


class DumpFileReader:
    def __init__(self, file_name):
        rv = RV32("32IV")
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

                        if not inst_hex.endswith("7"):
                            continue
                        
                        inst_decoder = rv.decodeHex(inst_hex)
                        inst_decoder = str(inst_decoder)

                        inst_compiler = "{} {}".format(inst_name, inst_params)

                        print("Actual: " + inst_compiler)
                        print("V32: " + inst_decoder)
                        
                        # Check predicted instruction is correct
                        assert inst_decoder == inst_compiler


def test_dump_file():
    files = glob(os.path.join("test_vec.dump"))
    for f in files:
        DumpFileReader(f)

test_dump_file();

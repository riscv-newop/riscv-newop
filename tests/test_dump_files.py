import string
import os
from glob import glob
from rvnewop import RV32

import pytest


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

                        inst_hex = words[1]
                        inst_name = words[2]
                        inst_params = words[3]

                        predicted_inst = rv.decodeHex(inst_hex)
                        predicted = str(predicted_inst)

                        inst = "{} {}".format(inst_name, inst_params)

                        # Check predicted instruction is correct
                        assert predicted == inst

                        print(
                            "{} == {}".format(
                                str(predicted_inst).split()[1], inst_params
                            )
                        )


def test_dump_file():
    # TODO seperate this into multiple functions
    # to see which ISAs failed
    files = glob(os.path.join("tests", "*.dump"))
    for file in files:
        DumpFileReader(file)

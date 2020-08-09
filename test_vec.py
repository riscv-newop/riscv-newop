#!/usr/bin/env python

import string
import os
from glob import glob
from rvnewop import RV32
from bitarray import bitarray

import pytest


class VectorCompare:
    def __init__(self, file_name):
        rv = RV32("32IV")
        if os.path.exists(file_name) == False:
            print("Fatal: Unable to find the file: " + file_name)
        else:
            hst_handle = open(file_name, "r")
            lines = hst_handle.readlines()
            for line in lines:
                words = line.split()

                inst_hex = words[4]

                inst = rv.decodeHex(inst_hex)
                inst = str(inst)

                predicted_inst_name = words[1]
                predicted_inst_params = words [2]

                predicted = "{} {}".format(predicted_inst_name, predicted_inst_params)
                
                print(predicted)
                print(inst)

                assert predicted == inst

def test_vec():
    files = ["test_vec.dat"]
    for f in files:
        VectorCompare(f)

test_vec()

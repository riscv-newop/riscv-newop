#!/usr/bin/env python3

#
# MOVE THIS FILE TO THE ROOT OF THE PROJECT TO RUN
#


import rvnewop as rv
import networkx as nx

# from tqdm import tqdm
from glob import glob

prog = rv.Program(name="liveness_test", isa="32IC")

# Create first basic block.
i1 = rv.RVInstruction(
            rv_format="R",
            rv_src_registers=["x10"],
            rv_dest_registers=["x10"],
            rv_name="addi",
            rv_size=32
        )
i2 = rv.RVInstruction(
            rv_format="B",
            rv_src_registers=["x10", "x11"],
            rv_immediates=[-4],
            rv_name="beq",
            rv_size=32
        )
i3 = rv.RVInstruction(
            rv_format="R",
            rv_src_registers=["x10"],
            rv_dest_registers=["x11"],
            rv_name="addi",
            rv_size=32
        )
prog.addInstructionObj(0x0, i1, 1)
prog.addInstructionObj(0x4, i2, 1)
prog.addInstructionObj(0x8, i3, 1)

prog.findBasicBlocks()

prog.printBasicBlocks()

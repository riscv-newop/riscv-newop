#!/usr/bin/env python3

#
# MOVE THIS FILE TO THE ROOT OF THE PROJECT TO RUN
#


import rvnewop as rv
import networkx as nx

# from tqdm import tqdm
from glob import glob

FILENAME = "./matmult-int.hst"

#for FILENAME in glob("./embench_hst/*.hst"):
print("Processing {}...".format(FILENAME))

prog = rv.Histogram.parse(FILENAME, isa="32ICM")
prog.findBasicBlocks()
prog.addLivenessValuesToGraph()

# total cycles = sum of all the frequencies
total_cycles = sum(
    [inst.freq for bb in prog.basicBlocks for inst in bb.bbInstructions()]
)

new_instructions = []

for i, b in enumerate((prog.getSubBlocks())):
    graph = b.constructDAG()

    # temp will store every permutation of candidate subgraphs
    temp = []
    for n in rv.analysis.findCandidateSubgraphs(prog, graph):
        subtree = rv.analysis.createSubtreeFromNode(graph, n)
        root = n

        temp.append(rv.Subgraph(subtree, root))

    # add candidate subgraph with highest score to new instructions list
    if temp:
        temp = sorted(temp, key=lambda sg: sg.score, reverse=True)
        new_instructions.append(temp[0])

saved_cycles = sum([sg.score for sg in new_instructions])
percent_cycles = float(saved_cycles) / total_cycles * 100

print(
    """Saved {} cycles out of {} ({:.4}%) with {} new instructions""".format(
        saved_cycles, total_cycles, percent_cycles, len(new_instructions)
    )
)

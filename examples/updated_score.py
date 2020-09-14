#!/usr/bin/env python3

#
# MOVE THIS FILE TO THE ROOT OF THE PROJECT TO RUN
#


import rvnewop as rv
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

# from tqdm import tqdm
from glob import glob

# FILENAME = "./embench_hst/aha-mont64.hst"

for FILENAME in glob("./embench_hst/*.hst"):
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
        current_nodes = set()
        temp = sorted(temp, key=lambda sg: sg.score, reverse=True)
        while temp:
            if any([(n in current_nodes) for n in temp[0].graph.nodes]):
                temp.pop(0)
            else:
                new_instructions.append(temp.pop(0))

    new_instructions = sorted(new_instructions, key=lambda sg: sg.score, reverse=True)

    inst_dict = {}
    for subgraph in new_instructions:
        key = rv.analysis.graphToParenString(subgraph.graph)

        if key in inst_dict:
            inst_dict[key].score += subgraph.score
        else:
            inst_dict[key] = subgraph

    new_instructions = [inst_dict[key] for key in inst_dict]

    saved_cycles = sum([sg.score for sg in new_instructions])
    percent_cycles = float(saved_cycles) / total_cycles * 100

    print(
        """Saved {} cycles out of {} ({:.4}%) with {} new instructions""".format(
            saved_cycles, total_cycles, percent_cycles, len(new_instructions)
        )
    )

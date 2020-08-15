#!/usr/bin/env python3
import rvnewop as rv
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout

from tqdm import tqdm

# FILENAME = "./examples/hst/pc_hist3.hst"
FILENAME = "./embench_hst/aha-mont64.hst"


prog = rv.Histogram.parse(FILENAME, isa="32ICM")
prog.findBasicBlocks()


i = 0
for b in tqdm(prog.getSubBlocks()):
    # for b in prog.getSubBlocks():
    graph = b.constructDAG()

    for n in rv.analysis.findCandidateSubgraphs(graph):
        plt.clf()
        sg = rv.analysis.createSubtreeFromNode(graph, n)

        # print(
        #     "{} hash: {} paren: {}".format(
        #         "output" + str(i) + ".png",
        #         rv.analysis.hashDAG(sg),
        #         rv.analysis.graphToParenString(sg),
        #     )
        # )

        pos = graphviz_layout(graph, prog="dot")
        nx.draw(sg, pos, with_labels=True, font_size=20)
        plt.savefig("output" + str(i) + ".png")
        i += 1

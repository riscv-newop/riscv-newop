import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt  # for graph visualization


class BasicBlock:
    """A class that contains the beginning and end of basic blocks"""

    def __init__(self, start, end, freq, instructions):
        """The start and end values are the pc values
           for the basic block begins and ends.
           freq is the count of how many times the block
           was executed.
           instructions is a dictionary of decoded instructions
           keyed by PC values. """

        self.start = start
        self.end = end
        self.frequency = freq
        self.instructions = instructions

    # TODO come up with a better name for this function??
    # People were right... there are only 3 hard problems in
    # computer science: cache invalidation, naming stuff,
    # and off-by-one errors.
    def bbInstructions(self):
        """A generator to loop through *only* the instructions
        contained in a basic block."""

        current = self.start
        while True:
            print(current)
            if current == self.end:
                # reached last instruction
                # return it and exit
                yield self.instructions[current]
                break
            else:
                yield self.instructions[current]
                current += self.instructions[current].size

    def constructDAG(self):
        """Construct Directed Acyclic Graph representation
        of the Basic Block"""

        graph = nx.DiGraph()
        registers = {
            reg
            for inst in self.bbInstructions()
            for reg in (inst.src_registers + inst.dest_registers)
        }
        print(registers)

        current_node = {reg: reg for reg in registers}
        graph.add_nodes_from(registers, type="register")

        for inst in self.bbInstructions():
            if not inst.dest_registers:
                # no dest registers, skip
                continue
            else:
                node = str(inst)
                graph.add_node(node, type="instruction", instruction=inst)
                for s in inst.src_registers:
                    graph.add_edge(current_node[s], node)

                for d in inst.dest_registers:
                    # set current to latest value
                    current_node[d] = node

        plt.clf()
        pos = graphviz_layout(graph, prog="dot")
        nx.draw(graph, pos, with_labels=True)
        plt.savefig("output.png")
        return graph

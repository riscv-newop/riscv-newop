from . import M32


class Subgraph:
    def __init__(self, graph, root):
        self.graph = graph
        self.root = root

        # the score is equal to the # of cycles saved
        # cycles saved = (number of instructions - 1) * frequency
        # number of instructions = total nodes - register nodes
        #
        # note: the root is guaranteed to not be a register node
        #       so we can savely get the instruction frequency from it
        #
        # another note: since these subgraphs come from the same basic block,
        #               all instructions in it are guaranteed to have the same
        #               frequency as all the rest
        self.score = (
            len(graph.nodes)
            - len([n for n in graph.nodes if graph.nodes[n]["type"] == "register"])
            - 1
        ) * graph.nodes[root]["instruction"].freq

        self.depth = self.calcDepth(self.root)
        
    def calcDepth(self, current):
        """Calculate the depth of a DAG recursively"""
        if len(list(self.graph.successors(current))) == 0:
            return 0
        return max([self.calcDepth(s) for s in self.graph.successors(current)]) + (1 if self.graph.nodes[current]['instruction'].name not in ['mv','c.mv'] else 0)

    def containsMultiplyInstruction(self):
        return any(
            [
                self.graph.nodes[node]["instruction"].name in M32.instructionNameSet
                for node in self.graph
                if self.graph.nodes[node]["type"] == "instruction"
            ]
        )

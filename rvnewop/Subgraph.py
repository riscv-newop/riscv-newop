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

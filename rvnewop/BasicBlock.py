import networkx as nx


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
        self.sub_blocks = []

    def genSubBlocks(self):
        """Generate subblocks within existing basic block

        Subblocks share the properties of a basic block but are broken up
        by load and store instructions as well as the normal jump and branch instructions."""
        pc = self.start
        s_pc = pc
        l_pc = None
        making_sub_block = True
        while pc <= self.end:
            insn = self.instructions[pc]
            if insn.isControlTransfer():
                if making_sub_block:
                    """ We are done making the sub-block """
                    if l_pc is not None:
                        self.sub_blocks.append(
                            BasicBlock(s_pc, l_pc, self.frequency, self.instructions)
                        )
                    making_sub_block = False
            elif insn.isMemAccess():
                if making_sub_block:
                    """ We are done making the sub-block """
                    if l_pc is not None:
                        self.sub_blocks.append(
                            BasicBlock(s_pc, l_pc, self.frequency, self.instructions)
                        )
                    making_sub_block = False
            else:
                if not making_sub_block:
                    s_pc = pc
                    making_sub_block = True
            l_pc = pc
            pc += insn.sizeInBytes()

        if making_sub_block:
            if l_pc is not None:
                self.sub_blocks.append(
                    BasicBlock(s_pc, l_pc, self.frequency, self.instructions)
                )

    def __str__(self):
        print("Start PC: " + hex(self.start))
        print("End PC: " + hex(self.end))

    # TODO come up with a better name for this function??
    # People were right... there are only 3 hard problems in
    # computer science: cache invalidation, naming stuff,
    # and off-by-one errors.
    def bbInstructions(self):
        """A generator to loop through *only* the instructions
        contained in a basic block."""

        current = self.start
        while True:
            # print(current)
            if current == self.end:
                # reached last instruction
                # return it and exit
                yield self.instructions[current]
                break
            else:
                yield self.instructions[current]
                current += self.instructions[current].sizeInBytes()

    def constructDAG(self):
        """Construct Directed Acyclic Graph representation
        of the Basic Block"""

        graph = nx.DiGraph()
        registers = {
            reg
            for inst in self.bbInstructions()
            for reg in (inst.src_registers + inst.dest_registers)
        }
        # print(registers)

        current_node = {reg: reg for reg in registers}
        graph.add_nodes_from(registers, type="register")

        for inst in self.bbInstructions():
            if not inst.dest_registers or inst.isControlTransfer():
                # no dest registers or control transfer, skip
                continue
            else:
                pc = list(self.instructions.keys())[
                    list(self.instructions.values()).index(inst)
                ]
                node = str(hex(pc)) + ": " + str(inst)
                graph.add_node(node, type="instruction", instruction=inst)
                for s in inst.src_registers:
                    graph.add_edge(node, current_node[s])

                for d in inst.dest_registers:
                    # set current to latest value
                    current_node[d] = node

        graph.remove_nodes_from([n for n, d in graph.degree if d == 0])
        if graph.number_of_nodes == 0:
            return None
        return graph

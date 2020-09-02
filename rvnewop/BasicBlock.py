import networkx as nx


class BasicBlock:
    """A class that contains the beginning and end of basic blocks"""

    def __init__(self, name, start, end, freq, instructions):
        """The start and end values are the pc values
           for the basic block begins and ends.
           freq is the count of how many times the block
           was executed.
           instructions is a dictionary of decoded instructions
           keyed by PC values. """

        self.name = name
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
        making_arith_block = True
        making_mem_block = False
        idx = 0
        while pc <= self.end:
            insn = self.instructions[pc]
            if insn.isControlTransfer():
                if making_arith_block or making_mem_block:
                    """ We are done making the sub-block """
                    """ Include this last control transfer PC in the sub-block """
                    self.sub_blocks.append(
                        BasicBlock(
                            self.name + "." + str(idx),
                            s_pc,
                            pc,
                            self.frequency,
                            self.instructions,
                        )
                    )
                    idx += 1
                    making_arith_block = False
                    making_mem_block = False
            elif insn.isMemAccess():
                if making_arith_block:
                    """ We are done making some previous sub-block """
                    if l_pc is not None:
                        self.sub_blocks.append(
                            BasicBlock(
                                self.name + "." + str(idx),
                                s_pc,
                                l_pc,
                                self.frequency,
                                self.instructions,
                            )
                        )
                        idx += 1

                    """ set s_pc for memory sub-block """
                    s_pc = pc
                    making_arith_block = False
                    making_mem_block = True
            else:
                if not making_arith_block:
                    """ Make a sub-block for mem accesses """
                    if making_mem_block:
                        self.sub_blocks.append(
                            BasicBlock(
                                self.name + "." + str(idx),
                                s_pc,
                                l_pc,
                                self.frequency,
                                self.instructions,
                            )
                        )
                        idx += 1
                        making_mem_block = False
                    s_pc = pc
                    making_arith_block = True
            l_pc = pc
            pc += insn.sizeInBytes()

        if making_arith_block or making_mem_block:
            if l_pc is not None:
                self.sub_blocks.append(
                    BasicBlock(
                        self.name + "." + str(idx),
                        s_pc,
                        l_pc,
                        self.frequency,
                        self.instructions,
                    )
                )
                idx += 1

    def __str__(self):
        print(self.name + ": Start PC: " + hex(self.start))
        print(self.name + ": End PC: " + hex(self.end))

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

    def getLiveRegisters(self):
        """Returns set of registers the basic block requires to be live as well as
        a set of registers that the basic block kills"""
        need_live = set()
        kills = set()
        for inst in self.bbInstructions():
            kills.update([x for x in inst.dest_registers if x])
            need_live.update([x for x in inst.src_registers if x and x not in killed])
        return (need_live, kills)

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

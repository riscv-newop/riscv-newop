from . import RV32
from . import BasicBlock

import sys
import networkx as nx


class Program:
    """A Program is a collection of instructions which are mapped to pc values"""

    def __init__(self, name, isa="32I"):
        self.name = name
        self.rv = RV32(isa=isa)
        self.instructions = {}  # maps pc value -> RVInstruction
        self.frequencies = {}  # maps pc value -> frequency of instruction

        # sets of names, registers, and formats for analysis
        self.instructionNameSet = set()
        self.registerSet = set()
        self.formatSet = set()
        self.basicBlocks = list()

        # list for liveness graph
        self.loop_backs = []

    def addInstruction(self, pc, hexd, freq):
        """Adds an instruction to a Program given a PC value
        and the instruction hex value

        pc - (int) program counter (pc)
        hexd - (str) instruction encoded in hexadecimal
        freq - (int) amount of times instruction shows up"""
        inst = self.rv.decodeHex(hexd)
        if not inst:
            print("ERROR decoding: {}".format(hexd))
            return
        inst.freq = freq
        self.instructions[pc] = inst
        if inst is None:
            print(hexd)

        # add to set as you go
        self.instructionNameSet.add(inst.name)
        self.registerSet.update(set(inst.src_registers) | set(inst.dest_registers))
        self.formatSet.add(inst.format)

        # TODO decouple storing frequencies from program?
        self.frequencies[pc] = freq

    def getTotalInstructionCount(self):
        total_ins = 0
        for pc in self.frequencies:
            total_ins += self.frequencies[pc]
        return total_ins

    def printAll(self, ofile=sys.stdout):
        """Prints out all instructions to file (default is stdout)"""
        for pc in self.instructions:
            print(
                "{} {}: {}".format(self.name, hex(pc), self.instructions[pc]),
                file=ofile,
            )

    def getNextUnvisited(self):
        min_pc = 2 * sys.maxsize + 1
        for pc in self.instructions:
            if not self.visited[pc]:
                if pc < min_pc:
                    min_pc = pc
        if min_pc < 2 * sys.maxsize + 1:
            return min_pc
        return None

    def createSubBlockGraph(self):
        self.sbGraph = nx.DiGraph()
        self.sbbd = dict()
        for block in self.basicBlocks
            for sbb in block.sub_blocks:
                s_pc = sbb.start
                self.sbbd[s_pc] = sbb
                n = sbb.name
                self.sbGraph.add_node(n, type="subblock", subblock=sbb, pc=s_pc)

        # add edges for sequential successors
        for pc in self.sbbd:
            e_pc = self.sbbd[pc].end
            n_pc = e_pc + self.instructions[e_pc].sizeInBytes()
            if n_pc in self.sbbd:
                self.sbGraph.add_edge(self.sbbd[pc].name, self.sbbd[n_pc].name)

        # add edges for branch targets
        for pc in self.sbbd:
            e_pc = self.sbbd[pc].end
            insn = self.instructions[e_pc]
            if insn.isControlTransferPCRelative():
                target_pc = e_pc + insn.immediates[0]
                if target_pc in self.sbbd:
                    self.sbGraph.add_edge(self.sbbd[pc].name, self.sbbd[target_pc].name)
        return

    def createBasicBlocks(self):
        idx = 0
        for entry in self.leader:
            if entry in self.instructions:
                start_pc = entry
                prev_pc = start_pc
                next_pc = prev_pc + self.instructions[start_pc].sizeInBytes()
                while next_pc in self.instructions and next_pc not in self.leader:
                    prev_pc = next_pc
                    next_pc = prev_pc + self.instructions[next_pc].sizeInBytes()
                bb = BasicBlock(
                    "B" + str(idx),
                    start_pc,
                    prev_pc,
                    self.frequencies[prev_pc],
                    self.instructions,
                )
                self.basicBlocks.append(bb)
                idx += 1
        for block in self.basicBlocks:
            block.genSubBlocks()

        self.createSubBlockGraph()

    def findBasicBlocks(self):
        self.visited = {}
        self.leader = {}
        for pc in self.instructions:
            self.visited[pc] = False

        explore_leader = []
        while self.getNextUnvisited() is not None:
            min_pc = self.getNextUnvisited()
            # first leader is the min_pc
            self.leader[min_pc] = True
            self.visited[min_pc] = True

            explore_leader.append(min_pc)
            while len(explore_leader):
                pc = explore_leader[0]
                explore_leader.remove(pc)
                if pc not in self.instructions:
                    continue
                """ scan sequentially starting at this PC
                    until one of:
                    - no next PC
                    - branch/jump
                    If no next PC, then we are done with this PC
                    If branch/jump, then add branch/jump destination as a leader
                    (if we know the address)
                    Also add the instruction following branch/jump PC as another
                    leader """
                insn = self.instructions[pc]
                end_of_sequence = False
                while not insn.isControlTransfer():
                    self.visited[pc] = True
                    pc = pc + insn.sizeInBytes()
                    if pc not in self.instructions:
                        end_of_sequence = True
                        break
                    insn = self.instructions[pc]
                if not end_of_sequence:
                    """we encountered a control transfer instruction
                    mark the next PC following the control transfer
                    as a leader"""
                    self.visited[pc] = True
                    leader_pc = pc + insn.sizeInBytes()
                    if leader_pc not in self.leader:
                        self.leader[leader_pc] = True
                        explore_leader.append(leader_pc)
                    """ we check if control transfer instruction is PC relative.
                        If yes, then we can determine the branch target address.
                        That address will be another leader. """
                    if insn.isControlTransferPCRelative():
                        target_pc = pc + insn.immediates[0]
                        if target_pc not in self.leader:
                            self.leader[target_pc] = True
                            explore_leader.append(target_pc)
        self.createBasicBlocks()

    def printBasicBlocks(self):
        print("Basic blocks in Program: " + self.name)
        for bb in self.basicBlocks:
            print(bb.name + " S: " + hex(bb.start))
            print(bb.name + " E: " + hex(bb.end))
            print([str(x) for x in bb.bbInstructions()])
            print("Sub-blocks in basic block:")
            for sbb in bb.sub_blocks:
                print(sbb.name + " S: " + hex(sbb.start))
                print(sbb.name + " E: " + hex(sbb.end))
                print([str(x) for x in sbb.bbInstructions()])

    def printSubBlocks(self):
        for pc in self.sbbd:
            sbb = self.sbbd[pc]
            print(sbb.name + " S: " + hex(sbb.start))
            print(sbb.name + " E: " + hex(sbb.end))

    def getSubBlocks(self):
        """Returns an array of subblocks"""
        return [
            subblock for bblock in self.basicBlocks for subblock in bblock.sub_blocks
        ]

    def setSubBlockLiveness(self, graph, current, add_live=set()):
        """Sets current node's liveness attributes"""
        (needs_live, kills) = self.sbbd[graph.nodes[current]["pc"]].getLiveRegisters()

        graph.nodes[current]["needs_live"] = needs_live | add_live
        graph.nodes[current]["kills"] = kills

    def depthFirstTraversalLiveness(self, graph, current):
        """Sets liveness values of a whole graph via a depth first traversal"""
        successors = graph.successors(current)

        # no children
        if len(list(successors)) == 0:
            self.setSubBlockLiveness(graph, current)
            return

        # has children
        else:
            (needs_live, kills) = self.sbbd[
                graph.nodes[current]["pc"]
            ].getLiveRegisters()

            add_live = set()
            for child in successors:
                # if child loops back, save its value and skip
                elif graph.nodes[child] < graph.nodes[current]:
                    self.loop_backs.append((current, child))
                else:
                    depthFirstTraversalLiveness(graph, child)
                    add_live.update(graph.nodes[child]["needs_live"] - kills)

            self.setSubBlockLiveness(graph, current, add_live=add_live)

    # TODO go back

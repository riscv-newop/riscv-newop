from . import RV32
from . import BasicBlock

import sys

class Program:
    """A Program is a collection of instructions which are mapped to pc values"""
    basicBlocks = []

    def __init__(self, name, isa="32I"):
        self.name = name
        self.rv = RV32(isa=isa)
        self.instructions = {}  # maps pc value -> RVInstruction
        self.frequencies = {}  # maps pc value -> frequency of instruction

        # sets of names, registers, and formats for analysis
        self.instructionNameSet = set()
        self.registerSet = set()
        self.formatSet = set()

    def addInstruction(self, pc, hexd, freq):
        """Adds an instruction to a Program given a PC value
        and the instruction hex value

        pc - (int) program counter (pc)
        hexd - (str) instruction encoded in hexadecimal
        freq - (int) amount of times instruction shows up"""
        inst = self.rv.decodeHex(hexd)
        self.instructions[pc] = inst

        # add to set as you go
        self.instructionNameSet.add(inst.name)
        self.registerSet.update(set(inst.src_registers) | set(inst.dest_registers))
        self.formatSet.add(inst.format)

        # TODO decouple storing frequencies from program?
        self.frequencies[pc] = freq

    def printAll(self, file=sys.stdout):
        """Prints out all instructions to file (default is stdout)"""
        for pc in self.instructions:
            print("{}: {}".format(hex(pc), self.instructions[pc]), file=file)

    def findBasicBlocks(self):
        min_pc = 2*sys.maxsize + 1
        visited = {}
        leader = {}
        for pc in self.instructions:
            visited[pc] = False
            if pc < min_pc:
                min_pc = pc
        # first leader is the min_pc
        leader[min_pc] = True
        visited[min_pc] = True
        print(self.name +':' + 'Discovered leader ' + hex(int(min_pc)))

        explore_leader = []
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
                pc = pc + insn.sizeInBytes()
                if pc not in self.instructions: 
                    end_of_sequence = True
                    break
                visited[pc] = True
                insn = self.instructions[pc]
            if not end_of_sequence:
                """ we encountered a control transfer instruction
                mark the next PC following the control transfer
                as a leader """
                visited[pc] = True 
                leader_pc = pc + insn.sizeInBytes()
                if leader_pc not in leader:
                    leader[leader_pc] = True
                    visited[leader_pc] = True 
                    explore_leader.append(leader_pc)
                    print(self.name +':' + 'Discovered leader ' + hex(int(leader_pc)))
                """ we check if control transfer instruction is PC relative.
                    If yes, then we can determine the branch target address.
                    That address wil be another leader. """
                if insn.isControlTransferPCRelative():
                    target_pc = pc + insn.immediates[0]
                    if target_pc not in leader:
                        print(self.name +':' + 'Discovered leader ' + hex(int(target_pc)))
                        leader[target_pc] = True
                        explore_leader.append(target_pc)

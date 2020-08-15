from . import I32
from . import M32
from . import RVFormatParser
from . import V32
from . import C32
from . import RVInstruction
from bitarray import bitarray


class RV32:
    """ General class for RISC-V 32bit """

    @staticmethod
    def composition(f1, f2):
        """Returns a composition of multiple instruction functions"""

        def f3(ba):
            # return first non-None value
            return next(x for x in [f1(ba), f2(ba)] if x)

        return f3

    def __init__(self, isa="32I"):
        """ A constructor for RV32
            isa is a string containing which instruction sets and extensions to use, by default this will use 32I"""

        # a mapping from frozenbitarray of opcode --> function that returns an RVInstruction
        self.instructionTable = {}
        self.instructionNameSet = set()
        self.registerSet = set()

        toAdd = []

        if "32I" in isa:
            # self.instructionTable.update(I32.instructionTable)
            toAdd.append(I32.instructionTable)
            self.instructionNameSet.update(I32.instructionNameSet)
            self.registerSet.update(I32.registerSet)
        if "M" in isa:
            # self.instructionTable.update(M32.instructionTable)
            toAdd.append(M32.instructionTable)
            self.instructionNameSet.update(M32.instructionNameSet)
        if "V" in isa:
            # self.instructionTable.update(V32.instructionTable)
            toAdd.append(V32.instructionTable)
            # TODO add inst name set
            # TODO add register set
        if "C" in isa:
            # self.instructionTable.update(C32.instructionTable)
            toAdd.append(C32.instructionTable)
            self.instructionNameSet.update(C32.instructionNameSet)

            # TODO maybe use decorators or some other syntatic sugar
            # to automate this?

        for table in toAdd:
            for key in table:
                if key in self.instructionTable:
                    self.instructionTable[key] = self.composition(
                        self.instructionTable[key], table[key]
                    )
                else:
                    self.instructionTable[key] = table[key]

    def decodeHex(self, hex):
        """Decode an instruction encoded in hexadecimal
        Returns RVInstruction"""
        bstr = bitarray(bin(int(hex, 16))[2:]).to01()
        size = 32

        # compressed instructions NEVER end in 11
        if bstr[-2:] != "11":
            size = 16

        bstr = bstr.zfill(size)
        ba = bitarray(bstr)

        return self.decode(ba, size)

    def decode(self, ba, size):
        """Decode an instruction encoded in binary as a bitarray
        Returns RVInstruction"""
        return self.instructionTable.get(
            RVFormatParser.getOpcode(ba), lambda x: RVInstruction(rv_name="error", rv_size=size)
        )(ba)

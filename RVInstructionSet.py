from abc import ABC, abstractmethod

# an abstract base class all instruction sets will inherit from
class RVInstructionSet(ABC):
    def __init__(self):
        self.instructionTable = {}

    #
    # the instruction table is a table mapped from opcodes -> functions that return an RVInstruction
    #
    @property
    @abstractmethod
    def instructionTable(self):
        return self.instructionTable

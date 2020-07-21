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

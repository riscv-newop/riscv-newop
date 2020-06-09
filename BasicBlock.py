class BasicBlock:
    """A class that contains the beginning and end of basic blocks"""

    def __init__(self, start, end):
        """The start and end values are the pc values
           for the basic block begins and ends"""
        self.start = start
        self.end = end

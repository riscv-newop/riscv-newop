from .Program import Program


class Histogram:
    """A Class to help parse .hst Histogram files and convert them into programs"""

    @staticmethod
    def parse(filename, isa="I32"):
        """Parses a given file and converts into a program"""
        program = Program(isa=isa)
        with open(filename) as infile:
            start = False

            for line in infile:
                if start:
                    values = line.split(" ")
                    pc = int(values[0], 16)
                    hex = values[1]
                    freq = int(values[2])
                    program.addInstruction(pc, hex, freq)

                if "PC Histogram size:" in line:
                    start = True

        return program

from . import Program


class Histogram:
    """A Class to help parse .hst Histogram files and convert them into programs"""

    @staticmethod
    def parse(self, filename, isa="I32"):
        """Parses a given file and converts into a program"""
        program = Program()
        with open(filename) as infile:
            for line in infile:
                if "PC Histogram size:" in line:
                    pass  # ignore size line

                values = line.split(" ")
                pc = int(values[0])
                hex = values[1]
                freq = int(values[2])

                program.addInstruction(pc, hex, freq)

        return program

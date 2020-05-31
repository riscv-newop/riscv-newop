import csv
from RV32 import RV32


def readHistogram(filename):

    rv = RV32()

    with open(filename) as csvf:
        reader = csv.reader(csvf, delimiter=" ")
        next(reader)
        next(reader)  # skip first two lines

        for row in reader:
            rv.addInstruction(row[0], bin(int(row[1], 16))[2:].zfill(32))

    return rv

import csv

from bitarray import bitarray

from . import RV32


def readHistogram(filename, isa="32I"):

    rv = RV32(isa)

    with open(filename) as csvf:
        reader = csv.reader(csvf, delimiter=" ")
        next(reader)
        next(reader)  # skip first two lines

        for row in reader:
            # converts hex pc string to int
            rv.addInstruction(
                int(row[0], 16), bitarray(bin(int(row[1], 16))[2:].zfill(32))
            )

    return rv

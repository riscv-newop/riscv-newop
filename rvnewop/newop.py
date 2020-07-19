import argparse
from glob import glob
from os import path

from .Histogram import Histogram

def newop():

    parser = argparse.ArgumentParser(
        description="Find new RISC-V Instructions from a histogram"
    )
    parser.add_argument("dirname", type=str, help="directory with .hst files in it")
    parser.add_argument(
        "--isa",
        type=str,
        dest="isa",
        help="which ISA and extensions to use, ex: 32IMCV",
    )

    args = parser.parse_args()

    files = glob(path.join(args.dirname, "*.hst"))
    programs = [Histogram.parse(file, isa=args.isa) for file in files]

    for program in programs:
        program.findBasicBlocks()

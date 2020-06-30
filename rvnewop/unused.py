import argparse
from glob import glob
from os import path

from .Histogram import Histogram
from .RV32 import RV32

from pprint import PrettyPrinter


def unused():

    parser = argparse.ArgumentParser(
        description="Find unused RISC-V Instructions from a histogram"
    )
    parser.add_argument("dirname", type=str, help="directory with .hst files in it")
    parser.add_argument(
        "--isa",
        type=str,
        dest="isa",
        help="which ISA and extensions to use, ex: 32IMCV",
    )

    args = parser.parse_args()

    files = glob(path.join(args.dirname), "*.hst")
    programs = [Histogram.parse(file, isa=args.isa) for file in files]

    inst_used = {}
    for program in programs:
        # populate inst_used
        inst_used.update(program.getInstructionNameSet())

    unused_inst = RV32(isa=args.isa).instructionNameSet - inst_used

    pp = PrettyPrinter(indent=4)
    pp.pprint(unused_inst)

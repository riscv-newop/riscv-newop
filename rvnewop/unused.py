import argparse
from glob import glob
from os import path
from pprint import PrettyPrinter

from .Histogram import Histogram


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

    files = glob(path.join(args.dirname, "*.hst"))
    programs = [Histogram.parse(file, isa=args.isa) for file in files]

    inst_used, reg_used = set(), set()
    for program in programs:
        # populate inst_used
        inst_used.update(program.getInstructionNameSet())
        reg_used.update(program.getRegisterSet())

    rv = programs[0].rv
    unused_inst = rv.instructionNameSet - inst_used
    unused_reg = rv.registerSet - reg_used

    pp = PrettyPrinter(indent=4)
    print("unused instructions:")
    pp.pprint(unused_inst)
    print("unused registers:")
    pp.pprint(unused_reg)

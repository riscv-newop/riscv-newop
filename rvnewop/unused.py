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
    format_ranges = dict.fromkeys(
        [format for program in programs for format in program.formatSet]
    )

    for program in programs:
        inst_used.update(program.instructionNameSet)
        reg_used.update(program.registerSet)

        for pc in program.instructions:
            inst = program.instructions[pc]
            if not inst.immediates:
                # no immediates in instruction
                continue

            # immediates is not empty
            cur_format = inst.format
            min_imm, max_imm = min(inst.immediates), max(inst.immediates)

            if format_ranges[cur_format] is None:
                format_ranges[cur_format] = (min_imm, max_imm)

            # check if min / max exist
            else:
                current_min, current_max = format_ranges[cur_format]
                format_ranges[cur_format] = (
                    min(min_imm, current_min),
                    max(max_imm, current_max),
                )

    rv = programs[0].rv
    unused_inst = rv.instructionNameSet - inst_used
    unused_reg = rv.registerSet - reg_used

    pp = PrettyPrinter(indent=4)
    print("unused instructions:")
    pp.pprint(unused_inst)
    print("unused registers:")
    pp.pprint(unused_reg)
    print("ranges for formats:")
    pp.pprint(format_ranges)

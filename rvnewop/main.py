import argparse

from .Histogram import Histogram


def main():
    parser = argparse.ArgumentParser(description="Disassemble RISC-V Assembly")
    parser.add_argument("filename", type=str, help="Histogram file to disassemble")
    parser.add_argument(
        "--save", dest="savefile", action="store", help="saves output to file"
    )

    parser.add_argument(
        "--isa",
        type=str,
        dest="isa",
        help="which ISA and extensions to use, ex: 32IMCV",
    )

    args = parser.parse_args()

    program = Histogram.parse(args.filename, args.isa)

    if args.savefile:
        with open(args.savefile) as f:
            program.printAll(f)
    else:
        program.printAll(f)

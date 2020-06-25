from .readHistogram import readHistogram
import argparse


def main():
    parser = argparse.ArgumentParser(description="Disassemble RISC-V Assembly")
    parser.add_argument(
        "filename", required=True, type=str, help="Histogram file to disassemble"
    )
    parser.add_argument(
        "--save", dest="savefile", action="store", help="saves output to file"
    )

    args = parser.parse_args()

    rv = readHistogram(args.filename)

    if args.savefile:
        with open(args.savefile) as f:
            rv.printAll(f)
    else:
        rv.printAll(f)

# riscv-newop
> A RISC_-V New Instruction Recommender System

## Installation
```commandline
# preferably inside of a venv
python3 -m pip install rvnewop
```

## Usage
```commandline
import rvnewop
from bitarray import bitarray

isa__model = renewop.RV32("32I")

hex = "00e787b3"
# TODO clean this process up
binary = bitarray(bin(int(hex, 16))[2:].zfill(32))
print(isa_model.decode(binary))
```

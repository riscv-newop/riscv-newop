# riscv-newop
> A RISC-V New Instruction Recommender System

## Installation
```commandline
# preferably inside of a venv
python3 -m pip install rvnewop
```

## Usage
```Python
from rvnewop import RV32
from bitarray import bitarray

isa_model = RV32("32I")

hex = "00e787b3"
# TODO clean this process up
binary = bitarray(bin(int(hex, 16))[2:].zfill(32))
print(isa_model.decode(binary))
```
output
```commandline
add x15 x15 x14
```

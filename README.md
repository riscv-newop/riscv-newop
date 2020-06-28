# riscv-newop
[![PyPI version](https://badge.fury.io/py/rvnewop.svg)](https://badge.fury.io/py/rvnewop)
[![Build Status](https://travis-ci.com/riscv-newop/riscv-newop.svg?branch=master)](https://travis-ci.com/riscv-newop/riscv-newop)
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

print(isa_model.decodeHex("00e787b3"))
```
output
```commandline
add a5,a5,a4
```

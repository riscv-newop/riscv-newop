import pytest
from bitarray import bitarray
from rvnewop import RV32


def test_add_example():
    rv = RV32("32I")
    binary = bitarray(bin(int("00e787b3", 16))[2:].zfill(32))

    assert str(rv.decode(binary)) == "add a5,a5,a4"

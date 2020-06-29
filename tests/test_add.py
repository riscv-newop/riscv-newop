import pytest
from bitarray import bitarray
from rvnewop import RV32


def test_add_example():
    rv = RV32("32I")
    assert str(rv.decodeHex("00e787b3")) == "add a5,a5,a4"

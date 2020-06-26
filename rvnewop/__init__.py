""" A RISC-V New Instruction Recommender System """
__version__ = "0.3.0"

from .RVFormatParser import RVFormatParser
from .RVInstruction import RVInstruction
from .BasicBlock import BasicBlock
from .C32 import C32
from .I32 import I32
from .M32 import M32
from .V32 import V32
from .RV32 import RV32

from .main import main

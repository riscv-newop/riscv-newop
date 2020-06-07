# TODO maybe remove rv_load_type
# TODO add rv_name for all the returns

from bitarray import bitarray, frozenbitarray

from RVFormatParser import RVFormatParser as fp
from RVInstruction import RVInstruction

class V32:
    """ A Class implementing the RV32V Standard Extension """

    @staticmethod
    def LOAD_FP(ba):
	    """Creates Vector Load Instructions"""
	    if fp.getMOP(ba) == "000" or fp.getMOP{ba} == "100":
	      data = fp.parseVL(ba)
  	    return RVInstruction(
		      rv_format="VL",
		      rv_src_registers=[data["rs1"]],
		      rv_dest_registers=[data["rd"]],
		      rv_mask=[data["vm"]],
		      rv_load_type="unit-stride",
		      rv_size=32,
		      rv_binary=ba,
	      )
	    elif fp.getMOP(ba) == "010" or fp.getMOP{ba} == "110":
	      data = fp.parseVLS(ba)
	      return RVInstruction(
          rv_format="VLS",
          rv_src_registers=[data["rs1"], data["rs2"]],
          rv_dest_registers=[data["rd"]],
          rv_mask=[data["vm"]],
          rv_load_type="strided",
          rv_size=32,
          rv_binary=ba,
	    )
	    elif fp.getMOP(ba) == "011" or fp.getMOP{ba} == "111":
	      data = fp.parseVLX(ba)
	      return RVInstruction(
          rv_format="VLX",
          rv_src_registers=[data["rs1"], data["vs2"]],
          rv_dest_registers=[data["rd"]],
          rv_mask=[data["vm"]],
          rv_load_type="indexed",
          rv_size=32,
          rv_binary=ba,
	    )
	    else
	      # TODO add error message?
	      pass

    # dictionary of opcodes --> functions(bitarray) --> RVInstruction
    instructionTable = {
        frozenbitarray("0000111"): LOAD_FP.__func__,
        frozenbitarray("0100111"): STORE_FP.__func__,
        frozenbitarray("0101111"): AMO.__func__,
        frozenbitarray("1010111"): OP_V.__func__,
    }

class RVInstruction:
    """A class to represent any RISC-V Instruction"""

    def __init__(
        self,
        rv_format=None,
        rv_src_registers=None,
        rv_dest_registers=None,
        rv_immediates=None,
	rv_nf=None,	#NEW
	rv_mask=None,	#NEW
	rv_width=None,	#NEW
        rv_sign=None, #NEW
        rv_umop=None,   #NEW
        rv_name=None,
        rv_size=None,
        rv_binary=None,
    ):
        """Constructs a RV Instruction based on parameters

            - format: the Instruction Format (i.e. R,I,S,B,U,J,etc)
            - src_registers: the registers read from
            - dest_registers: the registers written to
            - immediates: any constants used in the instruction
	    - nf: the number of fields in each segment for vector segment load/stores	#NEW
	    - mask: a vector instruction is masked if it does not modify the destination vector register element and never generates exceptions	#NEW
	    - width: the size of memory elements in vector instructions	#NEW
            - sign: indicates if a vector instruction is signed or unsigned
            - umop: indicates if a unit-stride vector load/store instruction is fault-only-first
            - name: the readable name of the instruction (i.e. addi, jal, beq, etc)
            - size: the size of the instruction in bits
            - binary: the original binary representation of the instruction
        """
        self.format = rv_format if rv_format is not None else ""
        self.src_registers = rv_src_registers if rv_src_registers is not None else []
        self.dest_registers = rv_dest_registers if rv_dest_registers is not None else []
        self.immediates = rv_immediates if rv_immediates is not None else []
	self.nf = rv_nf if rv_nf is not None else "None"	#NEW
	self.mask = rv_mask if rv_mask is not None else []	#NEW
	self.width = rv_width if rv_width is not None else "None"	#NEW
        self.sign = rv_sign if rv_sign is not None else ""    #NEW
        self.umop = rv_umop if rv_umop is not None else ""  #NEW
        self.name = rv_name if rv_name is not None else ""
        self.size = rv_size if rv_size is not None else 0
        self.binary = rv_binary if rv_binary is not None else ""

    def __str__(self):
        """Create a printable string from Instruction"""
        return " ".join(
            (
                self.name
#                + ("" if self.nf is None else self.nf)  # TODO fix nf in V32.py
#                + ("" if self.width is None else "".join(self.width))   #TODO width has to be encoded as b, h, w, e
#                + ("" if self.sign is None else "".join(self.sign))   #TODO properly define self.sign
#                + ("" if self.umop is None else "".join(self.umop)) #TODO fix ff in V32.py
#                + ("" if self.name[0] != "v" else ".v")   #TODO change this code to identify if it's a vector instruction (and maybe which kind as well)
#                + " "
		+ ("" if self.dest_registers is None else " ".join(self.dest_registers))
                + " "
                + ("" if self.src_registers is None else " ".join(self.src_registers))
                + " "
                + (
                    ""
                    if self.immediates is None
                    else " ".join(str(x) for x in self.immediates)
                )
            ).split()
        )

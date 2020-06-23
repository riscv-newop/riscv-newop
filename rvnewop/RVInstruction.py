class RVInstruction:
    """A class to represent any RISC-V Instruction"""

    def __init__(
        self,
        rv_format=None,
        rv_src_registers=None,
        rv_dest_registers=None,
        rv_immediates=None,
        rv_mask=None,
        rv_name=None,
        rv_size=None,
        rv_binary=None,
    ):
        """Constructs a RV Instruction based on parameters

            - format: the Instruction Format (i.e. R,I,S,B,U,J,etc)
            - src_registers: the registers read from
            - dest_registers: the registers written to
            - immediates: any constants used in the instruction
            - mask: a vector instruction is masked if it does not modify the destination vector register element and never generates exceptions
            - name: the readable name of the instruction (i.e. addi, jal, beq, etc)
            - size: the size of the instruction in bits
            - binary: the original binary representation of the instruction
        """
        self.format = rv_format if rv_format is not None else ""
        self.src_registers = rv_src_registers if rv_src_registers is not None else []
        self.dest_registers = rv_dest_registers if rv_dest_registers is not None else []
        self.immediates = rv_immediates if rv_immediates is not None else []
        self.mask = rv_mask if rv_mask is not None else ""
        self.name = rv_name if rv_name is not None else ""
        self.size = rv_size if rv_size is not None else 0
        self.binary = rv_binary if rv_binary is not None else ""

    def __str__(self):
        """Create a printable string from Instruction"""
        return " ".join(
            (
                self.name
                + " "
                + ("" if self.dest_registers is None else " ".join(self.dest_registers))
                + " "
                + ("" if self.src_registers is None else " ".join(self.src_registers))
                + " "
                + (
                    ""
                    if self.immediates is None
                    else " ".join(str(x) for x in self.immediates)
                )
                + " "
                + ("" if self.mask is None else self.mask)
            ).split()
        )

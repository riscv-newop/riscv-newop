class RVInstruction:
    """A class to represent any RISC-V Instruction"""

    def __init__(
        self,
        rv_format=None,
        rv_src_registers=None,
        rv_dest_registers=None,
        rv_immediates=None,
        rv_name=None,
        rv_size=None,
    ):
        """Constructs a RV Instruction based on parameters

            - format: the Instruction Format (i.e. R,I,S,B,U,J,etc)
            - src_registers: the registers read from
            - dest_registers: the registers written to
            - immediates: any constants used in the instruction
            - name: the readable name of the instruction (i.e. addi, jal, beq, etc)
            - size: the size of the instruction in bits
        """
        self.format = rv_format if rv_format is not None else ""
        self.src_registers = rv_src_registers if rv_src_registers is not None else []
        self.dest_registers = rv_dest_registers if rv_dest_registers is not None else []
        self.immediates = rv_immediates if rv_immediates is not None else []
        self.name = rv_name if rv_name is not None else ""
        self.size = rv_size if rv_size is not None else 0

    # TODO Check how valid this is, ie if order is correct
    def __str__(self):
        """Create a printable string from Instruction"""
        return "{} {} {} {}".format(
            self.name,
            " ".join(self.dest_registers),
            " ".join(self.src_registers),
            " ".join(self.immediates),
        )

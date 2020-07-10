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
        self.mask = rv_mask if rv_mask is not None else []
        self.name = rv_name if rv_name is not None else ""
        self.size = rv_size if rv_size is not None else 0
        self.binary = rv_binary if rv_binary is not None else ""

    @staticmethod
    def get_print_name(register_name):
        if register_name[0] == "x":
            xval = int(register_name[1:])
            if register_name == "x0":
                return "zero"
            elif register_name == "x1":
                return "ra"
            elif register_name == "x2":
                return "sp"
            elif register_name == "x3":
                return "gp"
            elif register_name == "x4":
                return "tp"
            elif register_name == "x5":
                return "t0"
            elif register_name == "x6":
                return "t1"
            elif register_name == "x7":
                return "t2"
            elif register_name == "x8":
                return "s0"
            elif register_name == "x9":
                return "s1"
            elif xval >= 10 and xval <= 17:
                return "a{}".format(xval - 10)
            elif xval >= 12 and xval <= 27:
                return "s{}".format(xval - 16)
            elif xval >= 28 and xval <= 31:
                return "t{}".format(xval - 25)

        # note: float registers have not been implemented
        # also vector registers
        return register_name

    def __str__(self):
        """Create a printable string from Instruction"""
        name = self.name
        dest = (
            []
            if self.dest_registers is None
            else [self.get_print_name(x) for x in self.dest_registers]
        )
        src = (
            []
            if self.src_registers is None
            else [self.get_print_name(x) for x in self.src_registers]
        )
        imm = [] if self.immediates is None else self.immediates
        mask = [] if self.mask is None else self.mask

        if name in [
            "lb",
            "lh",
            "lw",
            "lbu",
            "lhu",
            "sb",
            "sh",
            "sw",
            "c.lw",
            "c.sw",
            "c.lwsp",
            "c.swsp",
        ]:
            base = "sp" if name in ["c.lwsp", "c.swsp"] else src[0]
            parameters = ",".join(map(str, dest + src + imm + mask))
            return "{} {}({})".format(name, parameters, base).strip()

        parameters = ",".join(map(str, dest + src + imm + mask))
        return "{} {}".format(name, parameters).strip()

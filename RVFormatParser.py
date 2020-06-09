from bitarray import bitarray, frozenbitarray, util


class RVFormatParser:
    """class to parse different instruction formats (ie RISUBJ)"""

    # Helper methods to parse 32bit formats

    @staticmethod
    def getOpcode(ba):
        """ Creates frozenbitarray of opcode, used as a key in the instructionTable """
        return frozenbitarray(ba[-7:])

    @staticmethod
    def getRD(ba):
        """ Returns the destination register of a given instruction """
        return ba[-12:-7]

    @staticmethod
    def getFunct3(ba):
        """ Returns the funct3 of a given instruction,
        a funct3 further specifies what instruction a given opcode refers to"""
        return bitarray(ba[-15:-12])

    @staticmethod
    def getRS1(ba):
        """ Returns the first source register of an instruction """
        return ba[-20:-15]

    @staticmethod
    def getRS2(ba):
        """ Returns the second source register of an instruction """
        return ba[-25:-20]

    @staticmethod
    def getFunct7(ba):
        """ Returns the funct7 of an instruction,
            a funct7, like a funct3, further specifies what instruction an opcode refers to"""
        return bitarray(ba[:-25])

    # Vector methods

    @staticmethod
    def getNF(ba):
        """ Returns the number of fields in each segment for a given segment vector load/store instruction """
        return frozenbitarray(ba[:-29])

    @staticmethod
    def getMOP(ba):
        """ Returns the memory addressing mode of a given vector load/store instruction """
        return frozenbitarray(ba[-29:-26])

    @staticmethod
    def getVM(ba):
        """ Returns the vector mask of a given vector instruction """
        return frozenbitarray(ba[-26])

    @staticmethod
    def getAMOOP(ba):
        """ Returns the amoop of a given vector AMO instruction,
        a amoop specifies what AMO instruction a given opcode refers to """
        return frozenbitarray(ba[:-27])

    @staticmethod
    def getWD(ba):
        """ Returns the wd of a given vector AMO instruction,
        a wd specifies whether the original memory value is written to the vector destination register """
        return frozenbitarray(ba[-27])

    @staticmethod
    def getFunct6(ba):
        """ Returns the funct6 of a vector OP-V instruction,
        a funct6 specifies further specifies what instruction a given OP-V opcode refers to """
        return frozenbitarray(ba[:-26])

    @staticmethod
    def getVSetMSB(ba):
        """ Returns the MSB of a vector vset instruction """
        return frozenbitarray(ba[-32])

    @staticmethod
    def getVSetVLZeros(ba):
        """ Returns the six zeros of a vsetvl instruction """
        return frozenbitarray(ba[-31:-25])

    @staticmethod
    def convertToVectorRegister(ba):
        """ Takes in a bitarray or string of bits and converts it into a string specifying a vector register """
        return "v{}".format(util.ba2int(bitarray(ba)))

    # end of vector methods

    @staticmethod
    def convertToIntRegister(ba):
        """ Takes in a bitarray or string of bits and converts it into a string specifying an
            integer register """
        return "x{}".format(util.ba2int(bitarray(ba)))

    @staticmethod
    def twos_compliment(value, length):
        """ Returns the integer value of a number stored in two's complement """
        if (value & (1 << (length - 1))) != 0:
            value = value - (1 << length)
        return value

    @staticmethod
    def immToInt(imm):
        """Converts imm bitarray into twos complement integer"""
        return RVFormatParser.twos_compliment(int(bitarray(imm).to01(), 2), len(imm))

    # Compressed Helper methods
    # These help parse 16bit instructions

    @staticmethod
    def getCOpcode(ba):
        """Returns compressed opcode"""
        return ba[-2:]

    @staticmethod
    def getCFunct3(ba):
        """ Returns funct3 for CR format """
        return ba[:-13]

    # Parsing methods
    # These methods parse various formats via helper functions

    @staticmethod
    def parseR(ba):
        """ Parses the R format of instructions, Register to Register instructions """
        return {
            "funct7": RVFormatParser.getFunct7(ba),
            "rs2": RVFormatParser.convertToIntRegister(RVFormatParser.getRS2(ba)),
            "rs1": RVFormatParser.convertToIntRegister(RVFormatParser.getRS1(ba)),
            "funct3": RVFormatParser.getFunct3(ba),
            "rd": RVFormatParser.convertToIntRegister(RVFormatParser.getRD(ba)),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    @staticmethod
    def parseI(ba, convert=True):
        """ Parses the I format of instructions, Immediate to Register instructions """
        imm = RVFormatParser.getFunct7(ba) + RVFormatParser.getRS2(ba)
        return {
            "imm": RVFormatParser.immToInt(imm) if convert else imm,
            "rs1": RVFormatParser.convertToIntRegister(RVFormatParser.getRS1(ba)),
            "funct3": RVFormatParser.getFunct3(ba),
            "rd": RVFormatParser.convertToIntRegister(RVFormatParser.getRD(ba)),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    @staticmethod
    def parseU(ba):
        """ Parses the U format of instructions, examples: ECALL, EBREAK, etc """
        return {
            "imm": RVFormatParser.immToInt(bitarray(ba[:-12])),
            "rd": RVFormatParser.convertToIntRegister(RVFormatParser.getRD(ba)),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    @staticmethod
    def parseJ(ba):
        """ Parses the J format of instructions, Jump instructions """
        return {
            "imm": RVFormatParser.immToInt(
                bitarray(
                    bitarray(ba[-32])
                    + ba[-20:-12]
                    + bitarray(ba[-21])
                    + ba[-31:-21]
                    + "0"
                )  # adding 0 to the end is the same as left shifting by 1
            ),
            "rd": RVFormatParser.convertToIntRegister(RVFormatParser.getRD(ba)),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    @staticmethod
    def parseB(ba):
        """ Parses the B format of instructions, Branch instructions """
        return {
            "imm": RVFormatParser.immToInt(
                bitarray(
                    bitarray(ba[-32])
                    + bitarray(ba[-8])
                    + ba[-31:-25]
                    + ba[-12:-8]
                    + "0"
                )  # left shift by 1
            ),
            "rs2": RVFormatParser.convertToIntRegister(RVFormatParser.getRS2(ba)),
            "rs1": RVFormatParser.convertToIntRegister(RVFormatParser.getRS1(ba)),
            "funct3": RVFormatParser.getFunct3(ba),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    @staticmethod
    def parseS(ba):
        """ Parses the S format of instructions, Store instructions """
        return {
            "imm": RVFormatParser.immToInt(
                RVFormatParser.getFunct7(ba) + RVFormatParser.getRD(ba)
            ),
            "rs2": RVFormatParser.convertToIntRegister(RVFormatParser.getRS2(ba)),
            "rs1": RVFormatParser.convertToIntRegister(RVFormatParser.getRS1(ba)),
            "funct3": RVFormatParser.getFunct3(ba),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    # Parse compressed formats (CR, CI, CSS, etc)

    @staticmethod
    def parseCR(ba):
        """ Parses the CR format, Compressed Register instructions """
        return {
            "funct4": ba[:-12],
            "register": ba[-12:-7],  # can be rd or rs1 depending on instruction
            "rs2": ba[-7:-2],
            "op": RVFormatParser.getCOpcode(ba),
        }

    # end of compressed parsers

    # Vector parsers

    @staticmethod
    def parseVL(ba):
        """ Parses the Vector Load unit-stride format of instructions """
        return {
            "nf": RVFormatParser.getNF(ba),
            "mop": RVFormatParser.getMOP(ba),
            "vm": RVFormatParser.getVM(ba),
            "lumop": RVFormatParser.getRS2(ba),
            "rs1": RVFormatParser.convertToIntRegister(RVFormatParser.getRS1(ba)),
            "width": RVFormatParser.getFucnt3(ba),
            "vd": RVFormatParser.convertToVectorRegister(RVFormatParser.getRD(ba)),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    @staticmethod
    def parseVLS(ba):
        """ Parses the Vector Load strided format of instructions """
        return {
            "nf": RVFormatParser.getNF(ba),
            "mop": RVFormatParser.getMOP(ba),
            "vm": RVFormatParser.getVM(ba),
            "rs2": RVFormatParser.convertToIntRegister(RVFormatParser.getRS2(ba)),
            "rs1": RVFormatParser.convertToIntRegister(RVFormatParser.getRS1(ba)),
            "width": RVFormatParser.getFunct3(ba),
            "vd": RVFormatParser.convertToVectorRegister(RVFormatParser.getRD(ba)),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    @staticmethod
    def parseVLX(ba):
        """ Parses the Vector Load indexed format of instructions """
        return {
            "nf": RVFormatParser.getNF(ba),
            "mop": RVFormatParser.getMOP(ba),
            "vm": RVFormatParser.getVM(ba),
            "vs2": RVFormatParser.convertToVectorRegister(RVFormatParser.getRS2(ba)),
            "rs1": RVFormatParser.convertToIntRegister(RVFormatParser.getRS1(ba)),
            "width": RVFormatParser.getFunct3(ba),
            "vd": RVFormatParser.convertToVectorRegister(RVFormatParser.getRD(ba)),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    @staticmethod
    def parseVS(ba):
        """ Parses the Vector Store unit-stride format of instructions """
        return {
            "nf": RVFormatParser.getNF(ba),
            "mop": RVFormatParser.getMOP(ba),
            "vm": RVFormatParser.getVM(ba),
            "sumop": RVFormatParser.getRS2(ba),
            "rs1": RVFormatParser.convertToIntRegister(RVFormatParser.getRS1(ba)),
            "width": RVFormatParser.getFunct3(ba),
            "vs3": RVFormatParser.convertToVectorRegister(RVFormatParser.getRD(ba)),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    @staticmethod
    def parseVSS(ba):
        """ Parses the Vector Store strided format of instructions """
        return {
            "nf": RVFormatParser.getNF(ba),
            "mop": RVFormatParser.getMOP(ba),
            "vm": RVFormatParser.getVM(ba),
            "rs2": RVFormatParser.convertToIntRegister(RVFormatParser.getRS2(ba)),
            "rs1": RVFormatParser.convertToIntRegister(RVFormatParser.getRS1(ba)),
            "width": RVFormatParser.getFunct3(ba),
            "vs3": RVFormatParser.convertToVectorRegister(RVFormatParser.getRD(ba)),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    @staticmethod
    def parseVSX(ba):
        """ Parses the Vector Store indexed format of instructions """
        return {
            "nf": RVFormatParser.getNF(ba),
            "mop": RVFormatParser.getMOP(ba),
            "vm": RVFormatParser.getVM(ba),
            "vs2": RVFormatParser.convertToVectorRegister(RVFormatParser.getRS2(ba)),
            "rs1": RVFormatParser.convertToIntRegister(RVFormatParser.getRS1(ba)),
            "width": RVFormatParser.getFunct3(ba),
            "vs3": RVFormatParser.convertToVectorRegister(RVFormatParser.getRD(ba)),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    @staticmethod
    def parseVAMO(ba):
        """ Parses the Vector AMO format of instructions """
        return {
            "amoop": RVFormatParser.getAMOOP(ba),
            "wd": RVFormatParser.getWD(ba),
            "vm": RVFormatParser.getVM(ba),
            "vs2": RVFormatParser.convertToVectorRegister(RVFormatParser.getRS2(ba)),
            "rs1": RVFormatParser.convertToIntRegister(RVFormatParser.getRS1(ba)),
            "width": RVFormatParser.getFunct3(ba),
            "vd": RVFormatParser.convertToVectorRegister(RVFormatParser.getRD(ba)),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    @staticmethod
    def parseOPIVV(ba):
        """ Parses the Vector OPIVV format of instructions """
        return {
            "funct6": RVFormatParser.getFunct6(ba),
            "vm": RVFormatParser.getVM(ba),
            "vs2": RVFormatParser.convertToVectorRegister(RVFormatParser.getRS2(ba)),
            "vs1": RVFormatParser.convertToVectorRegister(RVFormatParser.getRS1(ba)),
            "funct3": RVFormatParser.getFunct3(ba),
            "vd": RVFormatParser.convertToVectorRegister(RVFormatParser.getRD(ba)),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    @staticmethod
    def parseOPFVV(ba):
        """ Parses the Vector OPFVV and OPMVV format of instructions """
        return {
            "funct6": RVFormatParser.getFunct6(ba),
            "vm": RVFormatParser.getVM(ba),
            "vs2": RVFormatParser.convertToVectorRegister(RVFormatParser.getRS2(ba)),
            "vs1": RVFormatParser.convertToVectorRegister(RVFormatParser.getRS1(ba)),
            "funct3": RVFormatParser.getFunct3(ba),
            # TODO how do I specify vd/rd?      "vd": RVFormatParser.convertToVectorRegister(RVFormatParser.getRD(ba)),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    @staticmethod
    def parseOPIVI(ba):
        """ Parses the Vector OPIVI format of instructions """
        return {
            "funct6": RVFormatParser.getFunct6(ba),
            "vm": RVFormatParser.getVM(ba),
            "vs2": RVFormatParser.convertToVectorRegister(RVFormatParser.getRS2(ba)),
            "simm5": RVFormatParser.immToInt(RVFormatParser.getRS1(ba)),
            "funct3": RVFormatParser.getFunct3(ba),
            "vd": RVFormatParser.convertToVectorRegister(RVFormatParser.getRD(ba)),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    @staticmethod
    def parseOPIVX(ba):
        """ Parses the Vector OPIVX and OPFVF format of instructions """
        return {
            "funct6": RVFormatParser.getFunct6(ba),
            "vm": RVFormatParser.getVM(ba),
            "vs2": RVFormatParser.convertToVectorRegister(RVFormatParser.getRS2(ba)),
            "rs1": RVFormatParser.convertToIntRegister(RVFormatParser.getRS1(ba)),
            "funct3": RVFormatParser.getFunct3(ba),
            "vd": RVFormatParser.convertToVectorRegister(RVFormatParser.getRD(ba)),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    @staticmethod
    def parseOPMVX(ba):
        """ Parses the Vector OPMVX format of instructions """
        return {
            "funct6": RVFormatParser.getFunct6(ba),
            "vm": RVFormatParser.getVM(ba),
            "vs2": RVFormatParser.convertToVectorRegister(RVFormatParser.getRS2(ba)),
            "rs1": RVFormatParser.convertToIntRegister(RVFormatParser.getRS1(ba)),
            "funct3": RVFormatParser.getFunct3(ba),
            # TODO how do I specify vd/rd?            "vd": RVFormatParser.convertToVectorRegister(RVFormatParser.getRD(ba)),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    @staticmethod
    def parseVSetVLI(ba):
        """ Parses the Vector vsetvli format of instructions """
        return {
            "vsetmsb": RVFormatParser.getVSetMSB(ba),
            "zimm": RVFormatParser.immToInt(
                RVFormatParser.getVSetVLZeros(ba) + RVFormatParser.getRS2(ba)
            ),
            "rs1": RVFormatParser.convertTIntRegister(RVFormatParser.getRS1(ba)),
            "funct3": RVFormatParser.getFunct3(ba),
            "rd": RVFormatParser.convertToIntRegister(RVFormatParser.getRD(ba)),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    @staticmethod
    def parseVSetVL(ba):
        """ Parses the Vector vsetvl format of instructions """
        return {
            "vsetmsb": RVFormatParser.getVSetMSB(ba),
            "vsetvlzeros": RVFormatParser.getVSetVLZeros(ba),
            "rs2": RVFormatParser.convertToIntRegister(RVFormatParser.getRS2(ba)),
            "rs1": RVFormatParser.convertTIntRegister(RVFormatParser.getRS1(ba)),
            "funct3": RVFormatParser.getFunct3(ba),
            "rd": RVFormatParser.convertToIntRegister(RVFormatParser.getRD(ba)),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    # end of vector parsers

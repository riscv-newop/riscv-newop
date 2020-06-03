from bitarray import bitarray, frozenbitarray, util


class RVFormatParser:
    """class to parse different instruction formats (ie RISUBJ)"""

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
                    ba[-32] + ba[-20:-12] + ba[-21] + ba[-31:-21] + "0"
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
                    ba[-32] + ba[-8] + ba[-31:-25] + ba[-12:-8] + "0"
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

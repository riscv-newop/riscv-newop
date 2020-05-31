from bitarray import frozenbitarray, bitarray, util


class RVFormatParser:
    """class to parse different instruction formats (ie RISUBJ)"""

    # Genral helper methods to parse formats
    @staticmethod
    def getOpcode(ba):
        return frozenbitarray(ba[-7:])

    @staticmethod
    def getRD(ba):
        return ba[-12:-7]

    @staticmethod
    def getFunct3(ba):
        return bitarray(ba[-15:-12])

    @staticmethod
    def getRS1(ba):
        return ba[-20:-15]

    @staticmethod
    def getRS2(ba):
        return ba[-25:-20]

    @staticmethod
    def getFunct7(ba):
        return bitarray(ba[:-25])

    @staticmethod
    def convertToIntRegister(ba):
        return "x{}".format(util.ba2int(bitarray(ba)))

    @staticmethod
    def twos_compliment(value, length):
        if (value & (1 << (length - 1))) != 0:
            value = value - (1 << length)
        return value

    @staticmethod
    def immToInt(imm):
        """Converts imm bitarray into twos complement integer"""
        return RVFormatParser.twos_compliment(int(bitarray(imm).to01(),2), len(imm))

    @staticmethod
    def parseR(ba):
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
        return {
            "imm": RVFormatParser.immToInt(bitarray(ba[:-12])),
            "rd": RVFormatParser.convertToIntRegister(RVFormatParser.getRD(ba)),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    @staticmethod
    def parseJ(ba):
        return {
            "imm": RVFormatParser.immToInt(
                bitarray(ba[-32] + ba[-20:-12] + ba[-21] + ba[-31:-21]
            )),
            "rd": RVFormatParser.convertToIntRegister(RVFormatParser.getRD(ba)),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    @staticmethod
    def parseB(ba):
        return {
            "imm": RVFormatParser.immToInt(bitarray(ba[-32] + ba[-8] + ba[-31:-25] + ba[-12:-6])),
            "rs2": RVFormatParser.convertToIntRegister(RVFormatParser.getRS2(ba)),
            "rs1": RVFormatParser.convertToIntRegister(RVFormatParser.getRS1(ba)),
            "funct3": RVFormatParser.getFunct3(ba),
            "opcode": RVFormatParser.getOpcode(ba),
        }

    @staticmethod
    def parseS(ba):
        return {
            "imm": RVFormatParser.immToInt(
                RVFormatParser.getFunct7(ba) + RVFormatParser.getRD(ba)
            ),
            "rs2": RVFormatParser.convertToIntRegister(RVFormatParser.getRS2(ba)),
            "rs1": RVFormatParser.convertToIntRegister(RVFormatParser.getRS1(ba)),
            "funct3": RVFormatParser.getFunct3(ba),
            "opcode": RVFormatParser.getOpcode(ba),
        }

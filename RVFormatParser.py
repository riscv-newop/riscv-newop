from bitarray import frozenbitarray, util


class RVFormatParser:
    """class to parse different instruction formats (ie RISUBJ)"""

    @staticmethod
    def getOpcode(ba):
        return frozenbitarray(ba[-7:])

    @staticmethod
    def convertToIntRegister(ba):
        return "x{}".format(util.ba2int(ba))

    @staticmethod
    def immToInt(imm):
        """Converts imm bitarray into twos complement integer"""
        return int.from_bytes(imm.tobytes(), byteorder="big", signed=True)

    @staticmethod
    def parseR(ba):
        return {
            "funct7": ba[:7],
            "rs2": RVFormatParser.convertToIntRegister(ba[7:12]),
            "rs1": RVFormatParser.convertToIntRegister(ba[12:17]),
            "funct3": ba[17:20],
            "rd": RVFormatParser.convertToIntRegister(ba[20:25]),
            "opcode": ba[25:32],
        }

    @staticmethod
    def parseI(ba, convert=True):
        return {
            "imm": RVFormatParser.immToInt(ba[:12]) if convert else ba[:12],
            "rs1": RVFormatParser.convertToIntRegister(ba[12:17]),
            "funct3": ba[17:20],
            "rd": RVFormatParser.convertToIntRegister(ba[20:25]),
            "opcode": ba[25:32],
        }

    @staticmethod
    def parseU(ba):
        return {
            "imm": RVFormatParser.immToInt(ba[:20]),
            "rd": RVFormatParser.convertToIntRegister(ba[20:25]),
            "opcode": ba[25:32],
        }

    @staticmethod
    def parseJ(ba):
        return {
            "imm": RVFormatParser.immToInt(
                ba[0] + ba[12:19] + ba[11] + ba[1:10]
            ),  # TODO check if correct
            "rd": RVFormatParser.convertToIntRegister(ba[20:25]),
            "opcode": ba[25:32],
        }

    @staticmethod
    def parseB(ba):
        return {
            "imm": RVFormatParser.immToInt(
                ba[0] + ba[25] + ba[1:7] + ba[20:24]
            ),  # TODO check if this is true
            "rs2": RVFormatParser.convertToIntRegister(ba[7:12]),
            "rs1": RVFormatParser.convertToIntRegister(ba[12:17]),
            "funct3": ba[17:20],
            "opcode": ba[25:32],
        }

    @staticmethod
    def parseS(ba):
        return {
            "imm": RVFormatParser.immToInt(ba[:7] + ba[20:25]),
            "rs2": RVFormatParser.convertToIntRegister(ba[7:12]),
            "rs1": RVFormatParser.convertToIntRegister(ba[12:17]),
            "funct3": ba[17:20],
            "opcode": ba[25:32],
        }

from RVInstruction import RVInstruction
from bitarray import frozenbitarray

# class to parse different instruction formats (ie RISUBJ)
class RVFormatParser:
    @staticmethod
    def getOpcode(ba):
        return frozenbitarray(ba[-7:])

    @staticmethod
    def convertToRegister(ba):
        pass

    @staticmethod
    def parseR(ba):
        pass

    @staticmethod
    def parseI(ba):
        pass

    @staticmethod
    def parseIShift(ba):
        pass

    @staticmethod
    def parseU(ba):
        pass

    @staticmethod
    def parseJ(ba):
        pass

    @staticmethod
    def parseB(ba):
        pass

    @staticmethod
    def parseS(ba):
        pass

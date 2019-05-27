# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets
import random
# from bitmap import BitMap
from PIL import Image

# definicja sumy xor
def xor(a, b):
    if int(a) - int(b) == 0:
        return 0
    else:
        return 1

class ScramblerDVB:
    def __init__(self, size_of_bitmap, raw_binary, label):
        self.sync = []
        self.scrambler_output = []
        self.descrambler_output = []
        self.first_sync = []
        self.raw_binary = raw_binary
        self.size_of_bitmap = size_of_bitmap
        self.SYNC_LENGTH = 15

        self.initialize_scrambler(label)


    # wypełnienie scramblera i wypisanie poczatkowych liczb pseudolosowych
    def initialize_scrambler(self, label):
        self.fill_sync()
        self.showInitialSeqInGUI(label)

    # Tworzenie sync/poczatkowe 15 pseudolosowych bitow w scramblerze
    def fill_sync(self):
        for i in range(self.SYNC_LENGTH):
            newRandom = random.randint(0, 1)
            self.sync.append(newRandom)
            self.first_sync.append(newRandom)

    # shows the first pseudo-random number seq
    def showInitialSeqInGUI(self, label):
        informal_sync = [str(i) for i in self.sync]
        label.append('\nInitial pseudo-random seq SYNC:    ' + ''.join(informal_sync))


    # funkcja scramblujaca
    def scramble(self):
        for i in range(len(self.raw_binary)):
            temp = len(self.sync)
            self.scrambler_output.append(xor(xor(self.sync[13], self.sync[14]), self.raw_binary[i]))
            while temp > 1:
                self.sync[temp-1] = self.sync[temp-2]
                temp -= 1
            self.sync[0] = xor(self.sync[13], self.sync[14])
        return self.scrambler_output


    # funkcja descramblujaca
    def descramble(self):
        for i in range(len(self.scrambler_output)):
            temp = len(self.first_sync)
            self.descrambler_output.append(xor(xor(self.first_sync[13], self.first_sync[14]), self.scrambler_output[i]))
            while temp > 1:
                self.first_sync[temp-1] = self.first_sync[temp-2]
                temp -= 1
            self.first_sync[0] = xor(self.first_sync[13], self.first_sync[14])
        return self.descrambler_output

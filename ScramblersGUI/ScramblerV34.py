import random


class ScramblerV34:
    def __init__(self, size_of_bitmap, raw_binary, textBrowserV34):
        self.sync = []
        self.scrambler_output = []
        self.descrambler_output = []
        self.first_sync = []
        self.raw_binary = raw_binary
        self.size_of_bitmap = size_of_bitmap
        self.SYNC_LENGTH = 23

        self.initialize_scrambler(textBrowserV34)


    #Definicja sumy XOR
    def xor(self, a, b):
        if int(a) - int(b) == 0:
            return 0
        else:
            return 1


    # fill the scrambler and print SYNC in GUI
    def initialize_scrambler(self, textBrowserV34):
        self.fill_sync()
        self.showInitialSeqInGUI(textBrowserV34)


    # creating the first 23 pseudo-random bit seq (SYNC)
    def fill_sync(self):
        for i in range(self.SYNC_LENGTH):
            newRandom = random.randint(0, 1)
            self.sync.append(newRandom)
            self.first_sync.append(newRandom)


    def showInitialSeqInGUI(self, textBrowserV34):
        informal_sync = [str(i) for i in self.sync]
        textBrowserV34.append('\nInitial pseudo-random seq SYNC:    ' + ''.join(informal_sync))


    # Scrambling function
    def scramble(self):
        for i in range(len(self.raw_binary)):
            temp = len(self.sync)
            tempo = self.xor(self.xor(self.sync[17], self.sync[22]), self.raw_binary[i])
            self.scrambler_output.append(tempo)
            while temp > 1:
                self.sync[temp-1] = self.sync[temp-2]
                temp -= 1
            self.sync[0] = tempo
        return self.scrambler_output


    # Descrambling function
    def descramble(self, noisedScramblerOutput):
        for i in range(len(noisedScramblerOutput)):
            temp = len(self.first_sync)
            self.descrambler_output.append(self.xor(self.xor(self.first_sync[17], self.first_sync[22]), noisedScramblerOutput[i]))
            while temp > 1:
                self.first_sync[temp-1] = self.first_sync[temp-2]
                temp -= 1
            self.first_sync[0] = noisedScramblerOutput[i]
        return self.descrambler_output

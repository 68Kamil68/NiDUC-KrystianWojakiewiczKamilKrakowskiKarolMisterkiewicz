import random


class ScramblerV34:
    def __init__(label):
        self.sync = []
        self.scrambler_output = []
        self.descrambler_output = []
        self.first_sync = []
        self.SYNC_LENGTH = 23

        self.initialize_scrambler(label)


    #Definicja sumy XOR
    def xor(self, a, b):
        if int(a) - int(b) == 0:
            return 0
        else:
            return 1

    # fill the scrambler and print SYNC in GUI
    def initialize_scrambler(self, label):
        self.fill_sync(self.sync, self.first_sync)
        self.showInitialSeqInGUI(label)


    # creating the first 23 pseudo-random bit seq (SYNC)
    def fill_sync(self, tab, tab2):
        for i in range(self.SYNC_LENGTH):
            newRandom = random.randint(0, 1)
            tab.append(newRandom)
            tab2.append(newRandom)


    def showInitialSeqInGUI(self, label):
        informal_sync = [str(i) for i in self.sync]
        label.append('\nInitial pseudo-random seq SYNC:    ' + ''.join(informal_sync))


    # Scrambling function
    def scrambling(self, tab):
        for i in range(len(tab)):
            temp = len(sync)
            tempo = xor(xor(sync[17], sync[22]), tab[i])
            self.scrambler_output.append(tempo)
            while temp > 1:
                self.sync[temp-1] = self.sync[temp-2]
                temp -= 1
            self.sync[0] = tempo
        return self.scrambler_output


    # Descrambling function
    def descrambling(self, tab):
        for i in range(len(tab)):
            temp = len(self.first_sync)
            self.descrambler_output.append(xor(xor(self.first_sync[17], self.first_sync[22]), tab[i]))
            while temp > 1:
                self.first_sync[temp-1] = self.first_sync[temp-2]
                temp -= 1
            self.first_sync[0] = self.scrambler_output[i]
        return self.descrambler_output






    #Pobranie słowa z pliku
    raw_binary = open('bintext.txt', 'r').read()
    print("Przed scramblingiem: " + raw_binary)

    #wykonanie scramblingu i wpisanie efektow
    scrambling(raw_binary)
    informal_scrambled = [str(i) for i in scrambler_output]
    print('Po scramblingu:      ' + ''.join(informal_scrambled))


    #wykonanie descramblingu i wpisanie efektow
    descrambling(scrambler_output)
    informal_descrambled = [str(i) for i in descrambler_output]
    print('Po descramblingu:    ' + ''.join(informal_descrambled))

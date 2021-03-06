import random
sync = []
scrambler_output = []
descrambler_output = []
first_sync = []

#Definicja sumy XOR
def xor(a, b):
    if int(a) - int(b) == 0:
        return 0
    else:
        return 1


#Tworzenie sync/poczatkowe 23 pseudolosowych bitow w scramblerze
def fill_sync(tab, tab2):
    for i in range(23):
        tab.append(random.randint(0, 1))
        tab2.append(tab[i])
    return tab




#wypełnienie scramblera i wypisanie poczatkowych liczb pseudolosowych
fill_sync(sync, first_sync)
informal_sync = [str(i) for i in sync]
print('\nCiag losowy SYNC:    ' + ''.join(informal_sync))

#Pobranie słowa z pliku
raw_binary = open('bintext.txt', 'r').read()
print("Przed scramblingiem: " + raw_binary)


#funkcja scramblujaca
def scrambling(tab):
    for i in range(len(tab)):
        temp = len(sync)
        tempo = xor(xor(sync[17], sync[22]), tab[i])
        scrambler_output.append(tempo)
        while temp > 1:
            sync[temp-1] = sync[temp-2]
            temp -= 1
        sync[0] = tempo
    return scrambler_output


#funkcja descramblujaca
def descrambling(tab):
    for i in range(len(tab)):
        temp = len(first_sync)
        descrambler_output.append(xor(xor(first_sync[17], first_sync[22]), tab[i]))
        while temp > 1:
            first_sync[temp-1] = first_sync[temp-2]
            temp -= 1
        first_sync[0] = scrambler_output[i]
    return descrambler_output


#wykonanie scramblingu i wpisanie efektow
scrambling(raw_binary)
informal_scrambled = [str(i) for i in scrambler_output]
print('Po scramblingu:      ' + ''.join(informal_scrambled))



#wykonanie descramblingu i wpisanie efektow
descrambling(scrambler_output)
informal_descrambled = [str(i) for i in descrambler_output]
print('Po descramblingu:    ' + ''.join(informal_descrambled))

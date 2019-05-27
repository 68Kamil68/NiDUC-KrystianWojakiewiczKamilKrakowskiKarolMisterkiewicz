# This Python file uses the following encoding: utf-8
import sys
import os
from PySide2.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtWidgets

import tkinter as tk
from tkinter.filedialog import askopenfilename


from PIL import Image

from ScramblerDVB import ScramblerDVB
from ScramblerAES import ScramblerAES

SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MainWindow(QtWidgets.QDialog):

    def __init__(self):
        #QMainWindow.__init__(self)
        super(MainWindow, self).__init__()
        uic.loadUi(os.path.join(SCRIPT_DIRECTORY, 'scramblergui.ui'), self)

        #setting up DVB event handlers
        self.loadFileBtnDVB.clicked.connect(self.loadButtonClicked)
        self.scrambleBtnDVB.clicked.connect(self.scrambleDVBButtonClicked)
        self.descrambleBtnDVB.clicked.connect(self.descrambleDVBButtonClicked)

        #setting up V34 event handlers
        self.loadFileBtnV34.clicked.connect(self.loadButtonClicked)
        #self.scrambleBtnV34.clicked.connect(self.scrambleV34ButtonClicked)
        #self.descrambleBtnV34.clicked.connect(self.descrambleV34ButtonClicked)

        #setting up AES event handlers
        self.loadFileBtnAES.clicked.connect(self.loadButtonClicked)
        self.scrambleBtnAES.clicked.connect(self.scrambleAESButtonClicked)
        #self.descrambleBtnAES.clicked.connect(self.descrambleAESButtonClicked)

        self.show()

        self.input_bnp = 0
        self.size_of_bitmap = 0
        self.raw_binary = []
        self.img = 0
        self.scramblerDVB = 0
        self.output_image = 0
        self.AES = 0


    #scramble AES button event handler
    def scrambleAESButtonClicked(self):
        self.AES = ScramblerAES()
        '''
        encryptedImage = self.AES.encrypt(self.img)

        self.output_image = Image.new('1', (self.size_of_bitmap, self.size_of_bitmap))
        pixels = self.output_image.load()
        for i in range(self.output_image.size[0]):    # For every pixel:
            for j in range(self.output_image.size[1]):
                pixels[i, j] = scrambledImage[(self.size_of_bitmap * i) + j]

        self.output_image.show(title='After AES')
        self.output_image = self.img.resize( (500, 500) )
        '''

    #scramble DVB button event handler
    def scrambleDVBButtonClicked(self):
        if self.size_of_bitmap == 0:
            return
        self.scramblerDVB = ScramblerDVB(self.size_of_bitmap, self.raw_binary)
        scrambledImage = self.scramblerDVB.scramble()
        informal_scrambled = [str(i) for i in self.scramblerDVB.scrambler_output]

        self.output_image = Image.new('1', (self.size_of_bitmap, self.size_of_bitmap))
        pixels = self.output_image.load()
        for i in range(self.output_image.size[0]):    # For every pixel:
            for j in range(self.output_image.size[1]):
                pixels[i, j] = scrambledImage[(self.size_of_bitmap * i) + j]

        self.output_image.show(title='After scrambling')
        self.output_image = self.img.resize( (500, 500) )

    #descramble DVB button event handler
    def descrambleDVBButtonClicked(self):
        #catch if no image to descramble
        if self.scramblerDVB == 0:
            return

        descrambledImage = self.scramblerDVB.descramble()
        self.output_image = Image.new('1', (self.size_of_bitmap, self.size_of_bitmap))
        pixels = self.output_image.load()

        for i in range(self.output_image.size[0]):    # For every pixel:
            for j in range(self.output_image.size[1]):
                pixels[i, j] = descrambledImage[(self.size_of_bitmap * i) + j]

        self.output_image.show(title='After descrambling')
        self.output_image = self.img.resize( (500, 500) )

    #load button event handler
    def loadButtonClicked(self):
        self.showLoadDialog()
        self.loadImage()

    #shows menu for choosing .bnp file
    def showLoadDialog(self):
        root = tk.Tk()
        root.withdraw()
        self.input_bnp = askopenfilename()

    # reading bitmap from file and writing pixel data into an array
    def loadImage(self):
        #return if no image was loaded
        if not self.input_bnp:
            return

        self.img = Image.open(self.input_bnp)
        self.size_of_bitmap = self.img.size[0]
        pixels = self.img.load()
        for i in range(self.img.size[0]):
            for j in range(self.img.size[1]):
                self.raw_binary.append(pixels[i, j])

        self.img = self.img.resize( (500, 500) )
        self.img.show(title='before scrambling')  # displaying input bitmap



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


######################################
######################################





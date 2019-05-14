# This Python file uses the following encoding: utf-8
import sys
import os
from PySide2.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtWidgets

import tkinter as tk
from tkinter.filedialog import askopenfilename


from PIL import Image
from Scrambler import Scrambler

SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MainWindow(QtWidgets.QDialog):

    def __init__(self):
        #QMainWindow.__init__(self)
        super(MainWindow, self).__init__()
        uic.loadUi(os.path.join(SCRIPT_DIRECTORY, 'scramblergui.ui'), self)

        self.loadFileBtn.clicked.connect(self.loadButtonClicked)
        self.scrambleBtn.clicked.connect(self.scrambleButtonClicked)
        self.descrambleBtn.clicked.connect(self.descrambleButtonClicked)
        self.show()

        self.input_bnp = 0
        self.size_of_bitmap = 0
        self.raw_binary = []
        self.img = 0
        self.scrambler= 0
        self.output_image = 0

    def scrambleButtonClicked(self):
        if self.size_of_bitmap == 0:
            return
        self.scrambler = Scrambler(self.size_of_bitmap, self.raw_binary)
        scrambledImage = self.scrambler.scramble()
        informal_scrambled = [str(i) for i in self.scrambler.scrambler_output]

        self.output_image = Image.new('1', (self.size_of_bitmap, self.size_of_bitmap))
        pixels = self.output_image.load()
        for i in range(self.output_image.size[0]):    # For every pixel:
            for j in range(self.output_image.size[1]):
                pixels[i, j] = scrambledImage[(self.size_of_bitmap * i) + j]

        self.output_image.show(title='Po scramblingu')
        self.output_image = self.img.resize( (500, 500) )


    def descrambleButtonClicked(self):
        if self.scrambler == 0:
            return

        descrambledImage = self.scrambler.descramble()
        self.output_image = Image.new('1', (self.size_of_bitmap, self.size_of_bitmap))
        pixels = self.output_image.load()

        for i in range(self.output_image.size[0]):    # For every pixel:
            for j in range(self.output_image.size[1]):
                pixels[i, j] = descrambledImage[(self.size_of_bitmap * i) + j]

        self.output_image.show(title='Po descramblingu')
        self.output_image = self.img.resize( (500, 500) )


    def loadButtonClicked(self):
        self.showLoadDialog()
        self.loadImage()

    #shows menu for choosing .bnp file
    def showLoadDialog(self):
        root = tk.Tk()
        root.withdraw()
        self.input_bnp = askopenfilename()

    # wczytanie bitmapy z plku i wprowadzenie wartosci pixeli do tablicy
    def loadImage(self):
        self.img = Image.open(self.input_bnp)
        self.size_of_bitmap = self.img.size[0]
        pixels = self.img.load()
        for i in range(self.img.size[0]):
            for j in range(self.img.size[1]):
                self.raw_binary.append(pixels[i, j])

        self.img = self.img.resize( (500, 500) )
        self.img.show(title='Przed  scramblingiem')  # wyswietlenie bitmapy wejsciowej



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


######################################
######################################





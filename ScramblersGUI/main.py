# This Python file uses the following encoding: utf-8
import sys
import os
from PySide2.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtWidgets, QtCore, QtGui


import tkinter as tk
from tkinter.filedialog import askopenfilename


from PIL import Image
from PIL.ImageQt import ImageQt

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
        encryptedImage = self.AES.encrypt( str(self.img) )
        self.textBrowser.append(str(encryptedImage))
        self.output_image = Image.new('1', (self.size_of_bitmap, self.size_of_bitmap))
        pixels = self.output_image.load()
        for i in range(self.output_image.size[0]):    # For every pixel:
            for j in range(self.output_image.size[1]):
                pixels[i, j] = encryptedImage[(self.size_of_bitmap * i) + j]



    #scramble DVB button event handler
    def scrambleDVBButtonClicked(self):
        if self.size_of_bitmap == 0:
            return
        self.scramblerDVB = ScramblerDVB(self.size_of_bitmap, self.raw_binary, self.textBrowserDVB)
        scrambledImage = self.scramblerDVB.scramble()
        informal_scrambled = [str(i) for i in self.scramblerDVB.scrambler_output]

        self.output_image = Image.new('1', (self.size_of_bitmap, self.size_of_bitmap))
        pixels = self.output_image.load()
        for i in range(self.output_image.size[0]):    # For every pixel:
            for j in range(self.output_image.size[1]):
                pixels[i, j] = scrambledImage[(self.size_of_bitmap * i) + j]

        self.showResultInGUI(self.afterImgLabelDVB, self.output_image)


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



    #load button event handler
    def loadButtonClicked(self):
        self.showLoadDialog()
        self.loadImage()


    #shows menu for choosing .bnp file
    def showLoadDialog(self):
        root = tk.Tk()
        root.withdraw()
        self.input_bnp = askopenfilename()
        self.showImageInGUI(self.beforeImgLabelAES, self.input_bnp)
        self.showImageInGUI(self.beforeImgLabelDVB, self.input_bnp)
        self.showImageInGUI(self.beforeImgLabelV34, self.input_bnp)


    # shows an image in the chosen label
    def showImageInGUI(self, label, imagePath):
        myPixmap = QtGui.QPixmap( imagePath )
        myScaledPixmap = myPixmap.scaled(label.size(), QtCore.Qt.KeepAspectRatio)
        label.setPixmap(myScaledPixmap)


    def showResultInGUI(self, label, image):
        #arr_uint8 = image_arr.astype(numpy.uint8)
        #im8 = Image.fromarray(arr_uint8)
        #imQt = QtGui.QImage(ImageQt.ImageQt(im8))
        imQt = QtGui.QImage(ImageQt(image))
        myPixmap = QtGui.QPixmap.fromImage( imQt )

        myScaledPixmap = myPixmap.scaled(label.size(), QtCore.Qt.KeepAspectRatio)
        label.setPixmap(myScaledPixmap)


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





if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


######################################
######################################





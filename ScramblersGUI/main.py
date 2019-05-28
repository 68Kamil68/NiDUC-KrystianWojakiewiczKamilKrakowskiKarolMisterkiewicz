# This Python file uses the following encoding: utf-8
import sys
import os
from PySide2.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtWidgets, QtCore, QtGui

import random
import numpy

import tkinter as tk
from tkinter.filedialog import askopenfilename


from PIL import Image
from PIL.ImageQt import ImageQt

from ScramblerDVB import ScramblerDVB
from ScramblerAES import ScramblerAES
from ScramblerV34 import ScramblerV34

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
        self.scrambleBtnV34.clicked.connect(self.scrambleV34ButtonClicked)
        self.descrambleBtnV34.clicked.connect(self.descrambleV34ButtonClicked)

        #setting up AES event handlers
        self.loadFileBtnAES.clicked.connect(self.loadButtonClicked)
        self.scrambleBtnAES.clicked.connect(self.scrambleAESButtonClicked)
        #self.descrambleBtnAES.clicked.connect(self.descrambleAESButtonClicked)

        self.show()

        self.input_bnp = 0
        self.size_of_bitmap = 0
        self.raw_binary = []
        self.img = 0

        self.probRatio = 3

        self.scramblerDVB = 0
        self.output_imageDVB = 0
        self.noisedImageDVB = 0

        self.AES = 0
        self.output_imageAES = 0
        self.noisedImageAES = 0

        self.scramblerV34 = 0
        self.output_imageV34 = 0
        self.noisedImageV34 = 0

        self.output_imageNoise = 0



    # scramble V34 button event handler
    def scrambleV34ButtonClicked(self):
        if self.size_of_bitmap == 0:    # return if no image found
            return

        self.scramblerV34 = ScramblerV34(self.size_of_bitmap, self.raw_binary, self.textBrowserV34)

        scrambledImage = self.scramblerV34.scramble()
        self.noisedImageV34 = self.addNoise(scrambledImage)

        self.output_imageV34 = Image.new('1', (self.size_of_bitmap, self.size_of_bitmap))
        pixels = self.output_imageV34.load()
        for i in range(self.output_imageV34.size[0]):    # For every pixel:
            for j in range(self.output_imageV34.size[1]):
                pixels[i, j] = self.noisedImageV34[(self.size_of_bitmap * i) + j]


        self.showResultInGUI(self.afterImgLabelV34, self.output_imageV34)


    # descramble V34 button event handler
    def descrambleV34ButtonClicked(self):
        if self.scramblerV34 == 0:   # return if scrambling hasn't been done
            return

        descrambledImage = self.scramblerV34.descramble(self.noisedImageV34)
        self.output_imageV34 = Image.new('1', (self.size_of_bitmap, self.size_of_bitmap))
        pixels = self.output_imageV34.load()

        for i in range(self.output_imageV34.size[0]):    # For every pixel:
            for j in range(self.output_imageV34.size[1]):
                pixels[i, j] = descrambledImage[(self.size_of_bitmap * i) + j]

        self.showResultInGUI(self.afterImgLabelV34, self.output_imageV34)


    # scramble AES button event handler
    def scrambleAESButtonClicked(self):
        if self.size_of_bitmap == 0:
            return

        self.AES = ScramblerAES(self.size_of_bitmap, self.raw_binary, self.textBrowserDVB)

        encryptedImageString = self.AES.encrypt()
        encryptedImageArray = numpy.asarray(encryptedImageString)

        self.output_imageAES = Image.new('1', (self.size_of_bitmap, self.size_of_bitmap))
        pixels = self.output_imageAES.load()
        for i in range(self.output_imageAES.size[0]):    # For every pixel:
            for j in range(self.output_imageAES.size[1]):
                pixels[i, j] = encryptedImage[(self.size_of_bitmap * i) + j]

        self.showResultInGUI(self.afterImgLabelAES, self.output_imageAES)

    # descramble AES button event handler
    def descrambleAESButtonClicked(self):
        if self.AES == 0:   # return if scrambling hasn't been done
            return


    #scramble DVB button event handler
    def scrambleDVBButtonClicked(self):
        if self.size_of_bitmap == 0:    # return if no image found
            return

        self.scramblerDVB = ScramblerDVB(self.size_of_bitmap, self.raw_binary, self.textBrowserDVB)
        scrambledImage = self.scramblerDVB.scramble()
        self.noisedImageDVB = self.addNoise(scrambledImage)

        self.output_imageDVB = Image.new('1', (self.size_of_bitmap, self.size_of_bitmap))
        pixels = self.output_imageDVB.load()
        for i in range(self.output_imageDVB.size[0]):    # For every pixel:
            for j in range(self.output_imageDVB.size[1]):
                pixels[i, j] = self.noisedImageDVB[(self.size_of_bitmap * i) + j]

        self.showResultInGUI(self.afterImgLabelDVB, self.output_imageDVB)


    #descramble DVB button event handler
    def descrambleDVBButtonClicked(self):
        if self.scramblerDVB == 0:  #catch if no image to descramble
            return

        descrambledImage = self.scramblerDVB.descramble(self.noisedImageDVB)
        self.output_imageDVB = Image.new('1', (self.size_of_bitmap, self.size_of_bitmap))
        pixels = self.output_imageDVB.load()

        for i in range(self.output_imageDVB.size[0]):    # For every pixel:
            for j in range(self.output_imageDVB.size[1]):
                pixels[i, j] = descrambledImage[(self.size_of_bitmap * i) + j]

        self.showResultInGUI(self.afterImgLabelDVB, self.output_imageDVB)


    #load button event handler
    def loadButtonClicked(self):
        self.showLoadDialog()
        self.loadImage()


    #shows menu for choosing .bnp file
    def showLoadDialog(self):
        root = tk.Tk()
        root.withdraw()
        self.input_bnp = askopenfilename()


    # shows an image in the chosen label
    def showImageInGUI(self, label, imagePath):
        myPixmap = QtGui.QPixmap( imagePath )
        myScaledPixmap = myPixmap.scaled(label.size(), QtCore.Qt.KeepAspectRatio)
        label.setPixmap(myScaledPixmap)


    def showResultInGUI(self, label, image):
        imQt = QtGui.QImage(ImageQt(image))
        myPixmap = QtGui.QPixmap.fromImage( imQt )

        myScaledPixmap = myPixmap.scaled(label.size(), QtCore.Qt.KeepAspectRatio)
        label.setPixmap(myScaledPixmap)


    # reading bitmap from file and writing pixel data into an array
    def loadImage(self):
        if not self.input_bnp:      #return if no image was loaded
            return

        self.raw_binary.clear()     # clearing raw_binary in case it wasn't empty

        self.img = Image.open(self.input_bnp)
        self.size_of_bitmap = self.img.size[0]
        pixels = self.img.load()
        for i in range(self.img.size[0]):
            for j in range(self.img.size[1]):
                self.raw_binary.append(pixels[i, j])

        noisedImage = self.addNoise(self.raw_binary)

        self.output_imageNoise = Image.new('1', (self.size_of_bitmap, self.size_of_bitmap))
        pixels = self.output_imageNoise.load()

        for i in range(self.output_imageNoise.size[0]):    # For every pixel:
            for j in range(self.output_imageNoise.size[1]):
                pixels[i, j] = noisedImage[(self.size_of_bitmap * i) + j]

        self.showResultInGUI(self.beforeImgLabelAES, self.output_imageNoise)
        self.showResultInGUI(self.beforeImgLabelDVB, self.output_imageNoise)
        self.showResultInGUI(self.beforeImgLabelV34, self.output_imageNoise)

        '''
        self.showImageInGUI(self.beforeImgLabelAES, self.input_bnp)
        self.showImageInGUI(self.beforeImgLabelDVB, self.input_bnp)
        self.showImageInGUI(self.beforeImgLabelV34, self.input_bnp)
        '''


    def addNoise(self, rawImage):
        zeroCounter = 0
        oneCounter = 0
        noisedImage = []
        for i in range( len(rawImage) ):
            if rawImage[i] == 0:
                zeroCounter += 1
                oneCounter = 0
            elif self.raw_binary[i] == 1:
                oneCounter += 1
                zeroCounter = 0

            noiseProb = (zeroCounter + oneCounter) / self.probRatio
            newRandom = random.randint(0, 100)
            if newRandom < noiseProb:
                noisedImage.append(~rawImage[i])
            else:
                noisedImage.append(rawImage[i])
        return noisedImage



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


######################################
######################################





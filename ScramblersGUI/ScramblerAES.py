# This Python file uses the following encoding: utf-8
from PySide2 import QtWidgets

import random
#import numpy

import hashlib
import base64

from PIL import Image

from Crypto import Random
from Crypto.Cipher import AES

AES_KEY_SIZE = 32

class ScramblerAES:
    def __init__(self, size_of_bitmap, raw_binary, textBrowserAES):
        self.AES_KEY_SIZE = 32
        self.size_of_bitmap = size_of_bitmap
        self.raw_binary = raw_binary
        self.raw = []
        self.outputImage = 0
        self.plaintext = ""
        self.encryptedCipher = 0

        key = str( random.getrandbits(AES_KEY_SIZE) )           # produce a string, which will be the key for AES
        self.key = hashlib.sha256(key.encode()).digest()        # we hash the key to make it more secure (more random)
        self.IV = Random.new().read(16)                         #


    # encrypt input image
    def encrypt(self):
        cipher = AES.new(self.key, AES.MODE_CFB, self.IV)  # creating AESCipher object for AES
        imageString = [str(i) for i in self.raw_binary]

        a = ""
        for i in range(len(self.raw_binary)):
            a += str(self.raw_binary[i])

        self.encryptedCipher = cipher.encrypt(str(a).encode())
        self.outputImage = Image.frombytes('1', (self.size_of_bitmap, self.size_of_bitmap), self.encryptedCipher)
        return self.outputImage


    #decrypt input image
    def decrypt(self):
        cipher = AES.new(self.key, AES.MODE_CFB, self.IV)                   # creating AESCipher object for AES

        decryptedImage = cipher.decrypt(self.encryptedCipher)

        b = []
        for i in range(len(decryptedString)):
              b.append(int(decryptedString[i]))
        print(b)
        return b


    def pad(self, s):
        while len(s) % self.AES_KEY_SIZE is not 0:
            s.append(1)
        return s#s.append((self.AES_KEY_SIZE - len(s) % self.AES_KEY_SIZE) * chr(49))#chr(self.AES_KEY_SIZE - len(s) % self.AES_KEY_SIZE)


    def unpad(self, s):
        return s[:-ord(s[len(s)-1:])]


    def showKeyInGUI(self, textBrowserAES):
        textBrowserAES.append("AES key: " + self.key)

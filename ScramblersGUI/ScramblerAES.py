# This Python file uses the following encoding: utf-8
from PySide2 import QtWidgets

import random
#import numpy

import hashlib
import base64


from Crypto import Random
from Crypto.Cipher import AES

AES_KEY_SIZE = 32

class ScramblerAES:
    def __init__(self, size_of_bitmap, raw_binary, textBrowserAES):
        self.AES_KEY_SIZE = 32
        self.size_of_bitmap = size_of_bitmap
        self.raw_binary = raw_binary
        self.output = []

        key = str( random.getrandbits(AES_KEY_SIZE) )           # produce a string, which will be the key for AES
        self.key = hashlib.sha256(key.encode()).digest()        # we hash the key to make it more secure (more random)
        self.IV = Random.new().read(16)                         #
        self.cipher = AES.new(self.key, AES.MODE_CBC, self.IV)  # creating AESCipher object for AES


    # encrypt input image
    def encrypt(self):
        imageString = ''.join(str(i) for i in self.raw_binary)
        paddedImage = self.pad(imageString)
        return self.cipher.encrypt(paddedImage)
        '''
        for i in range(len(self.raw_binary)):
            paddedPixel = self.pad( str(self.raw_binary[i]) )
            encryptedPixel = self.IV + self.cipher.encrypt(paddedPixel)
            self.output.append(encryptedPixel)
        return self.output
        '''

    #decrypt input image
    def decrypt(self, image):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')


    def pad(self, s):
        return s + (self.AES_KEY_SIZE - len(s) % self.AES_KEY_SIZE) * chr(self.AES_KEY_SIZE - len(s) % self.AES_KEY_SIZE)


    def unpad(self, s):
            return s[:-ord(s[len(s)-1:])]


    def showKeyInGUI(self, textBrowserAES):
        textBrowserAES.append("AES key: " + self.key)


'''
imageString = [str(i) for i in self.raw_binary]
paddedImage = self._pad( str(imageString) )
encryptedMessage = base64.b64encode(self.IV + self.cipher.encrypt(paddedImage))
'''

# This Python file uses the following encoding: utf-8
from PySide2 import QtWidgets

import random

import hashlib
import base64

from Crypto import Random
from Crypto.Cipher import AES

AES_KEY_SIZE = 32

class ScramblerAES:
    def __init__(self):
        self.AES_KEY_SIZE = 32

        key = str( random.getrandbits(AES_KEY_SIZE) )           # produce a string, which will be the key for AES
        self.key = hashlib.sha256(key.encode()).digest()        # we hash the key to make it more secure (more random)
        self.IV = Random.new().read(AES_KEY_SIZE)               # Add padding
        self.cipher = AES.new(self.key, AES.MODE_ECB, self.IV)  # creating AESCipher object for AES


    # encrypt input image
    def encrypt(self, image):
        image = self._pad(image)
        encryptedMessage = self.cipher.encrypt(image)
        return base64.b64encode(self.IV + encryptedMessage)


    #decrypt input image
    def decrypt(self, image):
        decryptedMessage = self.cipher.decrypt(image)
        return decryptedMessage


    def _pad(self, s):
        return s + (self.AES_KEY_SIZE - len(s) % self.AES_KEY_SIZE) * chr(self.AES_KEY_SIZE - len(s) % self.AES_KEY_SIZE)

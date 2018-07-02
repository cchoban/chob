from core import FileManager
import helpers
import hashlib


class main:
    def __init__(self, generate=False, token=None):
        self.isFirstTime = True
        self.token = token

        if self.keyExists():
            self.readToken()

        if generate:
            self.generateKey()

    def keyExists(self):
        key = FileManager.Manager().fileExists(helpers.getCobanPath+"\\.key")
        if key:
            return True
        else:
            return False

    def readToken(self):
        with open(helpers.getCobanPath+"\\.key", "r") as f:
            self.token = f.read()
            f.close()

    def generateKey(self):
        FileManager.Manager().createFile(helpers.getCobanPath+"\\.key", self.token, True)

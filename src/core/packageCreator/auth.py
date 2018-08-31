from core import FileManager
from core.cli import cli
from core.configurator import config
import helpers
import hashlib
from sys import exit


class main:

    def __init__(self, token=None, force=False):
        self.isFirstTime = True
        self.token = token
        self.force = force

    def init(self):
        if self.keyExists():
            if not self.force:
                self.printToken()
            else:
                self.generateKey()

    def keyExists(self):
        key = config.Configurator('auth_key')
        if key.key_exists():
            return True
        else:
            return False

    def readToken(self):
        key = config.Configurator()
        key.get_key('auth_key')
        self.token = key.get_key('auth_key')
        return self.token

    def printToken(self):
        key = config.Configurator()
        key.get_key('auth_key')

        if not self.force:
            helpers.successMessage(
                'Your auth key is: \'{}\'. If you want to change it use --force argument'.format(key.get_key('auth_key')))

    def generateKey(self):
        key = config.Configurator()
        key.setConfig('auth_key', self.token)

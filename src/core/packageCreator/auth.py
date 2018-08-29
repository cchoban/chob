from core import FileManager
from core.cli import cli
from core.configurator import config
import helpers
import hashlib
from sys import exit, argv


class main:

    def __init__(self, generate=False, token=None, force=False):
        self.isFirstTime = True
        self.token = token

        if self.keyExists():
            self.readToken()
            if force:
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

        if not '--force' in argv:
            helpers.successMessage(
                'Your auth key is: \'{}\'. If you want to change it use --force argument'.format(key.get_key('auth_key')))

    def generateKey(self):
        key = config.Configurator()
        key.setConfig('auth_key', self.token)

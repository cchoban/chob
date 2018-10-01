from core.configurator.config import Configurator
from helpers import redColor, packageInstallationPath, errorMessage, successMessage, getCobanPath
from os.path import abspath
from os import listdir
from core import JsonParser as js
from Logger import Logger as log
from hashlib import sha256, md5


class check:

    def __init__(self, hash, packageName, skipHashes, sandboxed=False, arches=False):
        self.hash = hash
        self.packageName = packageName
        self.skipHashes = skipHashes
        self.sandboxed = sandboxed
        self.arches = arches
        self.packagePath = "{0}\\{1}\\{1}".format(
            packageInstallationPath, self.packageName)
        self.files = {}
        self.prepare()

        if Configurator().get_key('skipHashByDefault', True):
            redColor(
                'Continues without checking hash. Because \'skipHashByDefault\' is set to \'true\'')
            self.skipHashes = True

    def prepare(self):
        self.parser = js.Parser(self.packagePath+'.cb').fileToJson()
        self.__is_sandboxed()
        self.__validate_keys()
        self.__files()
        self.calculate_package_hashes()

    def calculate_package_hashes(self):
        for file in self.files:
            self.hash = self.files[file]

            with open('{}\\packages\\{}\\{}'.format(getCobanPath, self.packageName, file), "rb") as f:
                calculatedHash = self.hashType(f.read()).hexdigest()

            if not self.hash.lower() == calculatedHash:
                if not self.skipHashes:
                    errorMessage(
                        "Hashes does not match with the uploaded version. If you want contiune add this argument '-skipHash'")
                    return False
                else:
                    redColor("Continues without checking hash.")
            elif self.skipHashes:
                redColor("Continues without checking hash.")
            else:
                successMessage("Hash(s) match for {}".format(file))

    def __files(self):
        if self.arches:
            arch64 = self.packageName+'x64.'+self.parser['packageArgs']['fileType']
            arch32 = self.packageName+'x86.' + self.parser['packageArgs']['fileType']

            files = {
                arch64: self.parser['packageArgs']['checksum64'],
                arch32: self.parser['packageArgs']['checksum']
            }

            self.files = {**self.files, **files}
        else:
            file = self.packageName+'.'+self.parser['packageArgs']['fileType']
            files = {
                file: self.checksum
            }

            self.files = {**self.files, **files}

    def __is_sandboxed(self):
        if self.sandboxed:
            self.packagePath = abspath(".package/{0}".format(self.packageName))

    def __validate_keys(self):
        parser = self.parser['packageArgs']
        if js.Parser().keyExists(parser, "downloadUrl64"):
            checksum = parser.get('checksum64')
            checksumType = parser.get('checksumType64')
        else:
            checksum = parser.get('checksum')
            checksumType = parser.get('checksumType')


        if not checksum and checksumType:
            errorMessage("Checksum keys are missing! Aborting.")
            exit()

        self.checksum = checksum
        self.checksumType = checksumType

        if checksumType == "sha256":
            self.hashType = sha256
        else:
            self.hashType = md5

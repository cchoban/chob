import helpers
import hashlib
from core import JsonParser as json
from Logger import Logger as log
from os.path import abspath
from sys import exit

class check:

    def __init__(self, hash, packageName, skipHashes, sandboxed=False):
        self.hash = hash
        self.skipHashes = skipHashes
        self.parseHash(packageName, sandboxed)
        self.calculate(packageName)
        self.packagePath = None
        self.hashType = None

    def parseHash(self, packageName, sandboxed=False):
        if sandboxed:
            self.packagePath = abspath(".package/{0}".format(packageName))
        else:
            self.packagePath = helpers.packageInstallationPath + \
                packageName + "\\" + packageName

        parser = json.Parser()

        loadJson = parser.fileToJson(self.packagePath + ".cb")["packageArgs"]

        try:
            if json.Parser().keyExists(loadJson, "downloadUrl64"):
                checksum = loadJson["checksum64"]
                checksumType = loadJson["checksumType64"]
            else:
                checksum = loadJson["checksum"]
                checksumType = loadJson["checksumType"]
        except KeyError as e:
            log.new(e).logError()
            helpers.errorMessage("Checksum keys are missing! Aborting.")
            exit()

        if checksumType == "sha256":
            self.hashType = hashlib.sha256
        else:
            self.hashType = hashlib.md5

    def calculate(self, packageName):
        parser = json.Parser()
        loadJson = parser.fileToJson(self.packagePath + ".cb")["packageArgs"]

        with open(self.packagePath + "." + loadJson["fileType"], "rb") as f:
            calculatedHash = self.hashType(f.read()).hexdigest()

        if not self.hash.lower() == calculatedHash:
            if not self.skipHashes == True:
                helpers.errorMessage(
                    "Hashes does not match with the uploaded version. If you want contiune add this argument '-skipHash'")
                exit()
            else:
                helpers.redColor("Continues without checking hash.")
        elif self.skipHashes == True:
            helpers.redColor("Continues without checking hash.")
        else:
            helpers.successMessage("Hashes match")

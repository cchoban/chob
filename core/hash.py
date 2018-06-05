import helpers, hashlib
from core import JsonParser as json
from Logger import Logger as log


class check:

    def __init__(self, hash, packageName, skipHashes):
        self.hash = hash
        self.skipHashes = skipHashes
        self.parseHash(packageName)
        self.calculate(packageName)
        self.hashType = None

    def parseHash(self, packageName):
        packagePath = helpers.packageInstallationPath + packageName + "\\" + packageName
        parser = json.Parser()

        loadJson = parser.fileToJson(packagePath + ".cb")["packageArgs"]

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
        packagePath = helpers.packageInstallationPath + packageName + "\\" + packageName
        parser = json.Parser()
        loadJson = parser.fileToJson(packagePath + ".cb")["packageArgs"]

        with open(packagePath + "." + loadJson["fileType"], "rb") as f:
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

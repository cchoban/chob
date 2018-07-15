import os
import json
import subprocess
from core import FileManager
import helpers
from sys import exit

class generateNewPackage:
    def __init__(self, packageName=None, generateFlatFileOnly=False):
        self.packageName = packageName
        self.softwareName = None
        self.description = None
        self.version = None
        self.enable64bit = False
        self.downloadUrl = None
        self.downloadUrl64 = None
        self.checksum = None
        self.checksum64 = None
        self.checksumType = None
        self.checksumType64 = None
        self.fileType = None
        self.silentArgs = None
        self.validExitCodes = []
        self.uninstallSilenArgs = None
        self.icon = None
        self.unzip = None
        self.dict = {}
        self.generateFlatFileOnly = generateFlatFileOnly

    def name(self):
        package = input("Package Name for application. Example: google-chrome*: ")
        self.packageName = package

    def sname(self):
        package = input("Software Name for application. Example: Google Chrome*: ")
        self.softwareName = package

    def desc(self):
        package = input("Description for application. This will be published on website*: ")
        self.description = package

    def ver(self):
        package = input("Version number for application. This will be published on website*: ")
        self.version = package

    def is64bit(self):
        package = input("Does this application has 64 bit product? [Y/N]*: ")

        if package == "y":
            self.enable64bit = True
        else:
            self.enable64bit = False

    def durl(self):
        if self.enable64bit:
            package64 = input("Download url for 64-bit product: ")
            self.downloadUrl64 = package64
        package = input("Download url for 32-bit product: ")
        self.downloadUrl = package

    def ctype(self):
        if self.enable64bit:
            checksumType64 = input("Checksum type for 64-bit application [sha256, md5]: ")
            self.checksumType64 = checksumType64

        checksumType = input("Checksum type for 32-bit application [sha256, md5]: ")
        self.checksumType = checksumType

    def checks(self):
        if self.enable64bit:
            checksum64 = input("Checksum for 64-bit application: ")
            self.checksum64 = checksum64

        checksumType = input("Checksum for 32-bit application: ")
        self.checksum = checksumType

    def filet(self):
        package = input("Filetype for application. Ex: [exe, msi, 7z, zip]: ")
        self.fileType = package

    def silenta(self):
        package = input("Silent args for application. Ex: [/S]: ")
        self.silentArgs = package

    def exitCodes(self):
        package = input(
            "Exit codes for application: (We detect if program exited successfully within this codes.) Example: 0,1,2: ")
        self.validExitCodes = package.split(",")

    def usilenta(self):
        package = input("Silent args for uninstallation of application. Ex: [/S]: ")
        self.uninstallSilenArgs = package

    def packageIcon(self):
        package = input("Icon URL for application: ")
        self.icon = package

    def isunzip(self):
        package = input("Is this application compressed with zip technologies? [Y/N]: ")
        if package == "y":
            self.unzip = True


class generatePackage(generateNewPackage):

    def getAnswers(self):
        if not self.generateFlatFileOnly:
            self.name()
            self.sname()
            self.desc()
            self.ver()
            self.is64bit()
            if not self.enable64bit:
                self.isunzip()
            self.durl()
            self.ctype()
            self.checks()
            self.filet()
            self.silenta()
            self.usilenta()
            self.exitCodes()
            self.packageIcon()

    def generateJson(self):

        dict = {
            "packageArgs": {
                "packageName": self.packageName,
                "softwareName": self.softwareName,
                "description": self.description,
                "version": self.version,
                "downloadUrl": self.downloadUrl,
                "checksum": self.checksum,
                "checksumType": self.checksumType,
                "fileType": self.fileType,
                "silentArgs": self.silentArgs,
                "validExitCodes": self.validExitCodes
            },

            "packageUninstallArgs": {
                "silentArgs": self.uninstallSilenArgs
            },

            "server": {
                "icon": self.icon
            }
        }

        if self.unzip != None and self.unzip == True:
            unzip = {
                "unzip": True
            }

            dict["packageArgs"].update(unzip)

        if self.generateFlatFileOnly or self.enable64bit:
            dict64 = {
                "downloadUrl64": self.downloadUrl64,
                "checksum64": self.checksum64,
                "checksumType64": self.checksumType64
            }

            dict["packageArgs"].update(dict64)

            self.dict = dict

        self.dict = dict

        return self.dict

    def __createPackageFolder(self, hidden=False):
        path = os.getcwd()
        if not self.packageName == None:
            FileManager.Manager().createFolder(path + "\\" + self.packageName)
            FileManager.Manager().createFolder(path + "\\" + self.packageName + "\\icons")
        else:
            FileManager.Manager().createFolder(path + "\\package")
            FileManager.Manager().createFolder(path + "\\icons")

    def __createPackageFiles(self):
        path = os.getcwd() + "\\"
        if not self.packageName == None:
            path = os.getcwd() + "\\" + self.packageName + "\\"

        FileManager.Manager().createFile(path + ".packagable", "Choban package manager", True)

    def writeToFile(self, dict={}):
        self.__createPackageFolder(True)
        self.__createPackageFiles()
        if self.dict:
            dict = self.dict
        else:
            dict = dict

        if not self.packageName == None:
            path = os.getcwd() + "\\{0}\\{1}.cb".format(self.packageName, self.packageName)
        else:
            path = os.getcwd() + "\\{0}.cb".format(self.packageName)
        with open(path, "w") as f:
            f.write(json.dumps(dict, indent=4))
            f.close()

#
# try:
#     cls = generatePackage()
#     cls.getAnswers()
#     dict = cls.generateJson()
#     cls.writeToFile(dict)
#
#     print(generateNewPackage().packageName)
# except Exception as e:
#     print(e)
#     pass
#

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
        self.only64bit = None
        self.generateFlatFileOnly = generateFlatFileOnly
        self.dependencies = []
        self.createShortcut = None
        self.createShortcut64 = None
        self.author = None
        self.lisence = None
        self.path = []
        self.envs = {}

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

    def only64(self):
        package = input('Is this application 64-bit only? [Y/N]*: ')

        if package == 'y':
            self.only64bit = True
        else:
            self.only64bit = False

    def durl(self):
        if self.enable64bit:
            package64 = input("Download url for 64-bit product: ")
            self.downloadUrl64 = package64
        if not self.only64bit:
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

    def deps(self):
        package = input(
            "Dependencies for {}. Example: git,nodejs: ".format(self.packageName))
        if len(package) > 0:
            self.dependencies = package.split(",")
        else:
            return []

    def shortcut(self):
        package = input(
            "Shortcuts for {}. This will help user to run command from his command line. Example: php.exe, php.ini: ".format(self.packageName))

        if len(package) > 0:
            self.createShortcut = package.split(",")
        else:
            return []


        if self.enable64bit:
            package = input(
                "Shortcuts for {} (64-Bit). This will help user to run command from his command line. Example: php.exe, php.ini: ".format(self.packageName))
            if len(package) > 0:
                self.createShortcut64 = package.split(",")
            else:
                return []

    def author_page(self):
        package = input(
            "Author or webpage for {}: ".format(self.packageName))

        self.author = package

    def package_lisence(self):
        package = input(
            "Package lisence for {}: ".format(self.packageName))

        self.lisence = package

    def path_envs(self):
        package = input('Paths to be added to PATH environment. Example: {cobanTools}\\php\: ')
        if len(package) > 0:
                self.path = package.split(",")
        else:
            return []

    def environments(self):
        package = input('Environment keys to be added. Example: NVM_SYMLINK={cobanTools}\\php: ')

        if len(package) > 0:
            self.envs = dict(x.split('=') for x in package.split(','))
        else:
            return {}

class generatePackage(generateNewPackage):

    def getAnswers(self):
        if not self.generateFlatFileOnly:
            self.sname()
            self.desc()
            self.ver()
            self.only64()
            if not self.only64bit:
                self.is64bit()
            self.isunzip()
            self.durl()
            self.ctype()
            self.checks()
            self.filet()
            self.deps()
            if self.unzip:
                self.shortcut()
                self.environments()
                self.path_envs()
            self.author_page()
            self.package_lisence()
            if not self.unzip:
                self.silenta()
                self.usilenta()
                self.exitCodes()
            self.packageIcon()


    def generateJson(self):

        root = {
            "packageArgs": {
                "packageName": self.packageName,
                "softwareName": self.softwareName,
                "description": self.description,
                "version": self.version,
                "downloadUrl": self.downloadUrl,
                "checksum": self.checksum,
                "checksumType": self.checksumType,
                "fileType": self.fileType,
                "dependencies": self.dependencies,
                'author': self.author,
                'lisence': self.lisence,
                'environments': self.envs,
                'path_env': self.path
            },

            'packageUninstallArgs': {
                'silentArgs': self.uninstallSilenArgs
            },

            "server": {
                "icon": self.icon
            }
        }

        if not self.unzip:
            root['packageArgs']['silentArgs'] = self.silentArgs
            root['packageArgs']['validExitCodes'] = self.validExitCodes

        if self.only64bit:
            root['packageArgs']['64bitonly'] = True

        if self.unzip != None and self.unzip == True:
            root['packageArgs']['unzip'] = True

            if self.createShortcut:
                root['packageArgs']['createShortcut'] = {
                    '32bit': self.createShortcut
                }

        if self.enable64bit:
            if self.unzip:
                root['packageArgs']['createShortcut'].update({
                    '64bit': self.createShortcut64
                })

        if self.generateFlatFileOnly or self.enable64bit:
            dict64 = {
                "downloadUrl64": self.downloadUrl64,
                "checksum64": self.checksum64,
                "checksumType64": self.checksumType64
            }

            root["packageArgs"].update(dict64)

            self.dict = root

        self.dict = root

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

        if not self.packageName == None:
            path = os.getcwd() + "\\{0}\\{1}.cb".format(self.packageName, self.packageName)
        else:
            path = os.getcwd() + "\\{0}.cb".format(self.packageName)
        with open(path, "w") as f:
            f.write(json.dumps(self.dict, indent=4, sort_keys=True))
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

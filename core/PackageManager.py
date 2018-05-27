import subprocess, sys, hashlib, helpers
from . import http
from . import FileManager as file
from . import JsonParser as json
from windows import winregistry
from . import hash


class Manager:
    def __init__(self, packageName, skipHashes, force):
        self.packageName = packageName
        self.skipHashes = skipHashes
        self.forceInstallation = force
        self.packageScriptName = self.packageName + ".cb"
        self.packagePathWithExt = helpers.packageInstallationPath + packageName + "\\" + packageName + ".cb"
        self.packagePathWithoutExt = helpers.packageInstallationPath + packageName + "\\" + packageName

        self.parser = json.Parser
        if file.Manager.fileExists(self.packagePathWithExt):
            self.scriptFile = self.parser.fileToJson(self.parser, self.packagePathWithExt)["packageArgs"]

    def installPackage(self):
        installable = {
            "exe": self.installExecutable,
            "msi": self.installExecutable,
            "unzip": self.unzipPackage
        }

        print(helpers.colors.fg.lightgrey + "Installing following packages:" + helpers.colors.reset)
        helpers.successMessage(self.packageName)
        print(
            helpers.colors.fg.lightgrey + "By installing you accept licenses for the packages." + helpers.colors.reset)

        self.agreement()
        self.isInstalled()
        self.getInstallationScript()
        self.downloadDependencies()
        self.checkHash()

        for i in installable:
            if json.Parser.keyExists(self.scriptFile, i) or self.scriptFile["fileType"] == i:
                return installable[i]()

    def isInstalled(self):
        if file.Manager.fileExists(self.packagePathWithExt):
            helpers.infoMessage(
                "You already installed this package. You can upgrade it by 'coban upgrade " + self.packageName + ""
                "' or by adding '--force' argument to force installation")

            if not self.forceInstallation:
                exit()

    def agreement(self):

        yes = {'yes', 'y', 'ye', ''}
        no = {'no', 'n'}

        choice = input("Do you want to install " + self.packageName + "? [Y/N]").lower()
        if choice in yes:
            return True
        elif choice in no:
            exit()
        else:
            sys.stdout.write("Please respond with 'yes' or 'no'")
            exit()

    def getInstallationScript(self):
        try:
            if self.isInstalled():
                return self.packagePathWithExt

            packageUrl = helpers.programList()[self.packageName]
            file.Manager.createFolder(helpers.packageInstallationPath + self.packageName)
            helpers.infoMessage("Downloading Installation Script of: " + self.packageScriptName)
            http.Http.download(http.Http, packageUrl,
                               helpers.packageInstallationPath + self.packageName + "\\" + self.packageScriptName, "")
            self.scriptFile = self.parser.fileToJson(self.parser, self.packagePathWithExt)["packageArgs"]
        except KeyError as e:
            e = "This program does not exists on your list. Please update your lists with 'coban update' "
            helpers.errorMessage(e)
            exit()

    def downloadDependencies(self):
        httpClass = http.Http

        loadJson = self.scriptFile
        if not file.Manager.fileExists(self.packagePathWithoutExt + "." + loadJson["fileType"]):
            if helpers.is_os_64bit() and self.parser.keyExists(self.scriptFile, "downloadUrl64"):
                if self.parser.keyExists(loadJson, "downloadUrl64"):
                    helpers.infoMessage("Downloading " + self.packageName + " from: " + loadJson["downloadUrl64"])
                    httpClass.download(httpClass, loadJson["downloadUrl64"], self.packagePathWithoutExt,
                                       loadJson["fileType"])
            else:
                helpers.infoMessage("Downloading " + self.packageName + " from: " + loadJson["downloadUrl"])
                httpClass.download(httpClass, loadJson["downloadUrl"], self.packagePathWithoutExt, loadJson["fileType"])

    def removePackage(self):
        print(helpers.colors.fg.lightgrey + "Removing following packages:" + helpers.colors.reset)
        helpers.redColor(self.packageName)

        self.uninstallExecutable(self.packageName)
        self.cleanLeftOvers(self.packageName)
        helpers.successMessage("Successfully removed " + self.packageName)

    def installExecutable(self):
        helpers.infoMessage(
            "Installing " + self.packageName + ". This will take a moment depends on software your installing. ")

        subprocess.call(self.packagePathWithoutExt + "." + self.scriptFile["fileType"] + " " + self.scriptFile["silentArgs"], shell=True)
        self.parser.addNewPackage(self.parser, self.packageName)
        helpers.successMessage("Successfully installed " + self.packageName)

    def uninstallExecutable(self):
        reg = winregistry.Registry
        package = reg.searchForSoftware(reg, self.packageName)

        subprocess.call(package["UninstallString"] + " " + self.scriptFile["packageUninstallArgs"]["silentArgs"])
        self.parser.removePackage(self.packageName)

    def cleanLeftOvers(self):
        packagePath = helpers.packageInstallationPath + self.packageName
        fileManager = file.Manager
        fileManager.removeDir(fileManager, packagePath)

    def unzipPackage(self):
        extensions = {
            "7z": file.Manager.extract7z,
            "zip": file.Manager.extractZip
        }

        fileName = self.packageName + "." + self.scriptFile["fileType"]
        zipFile = helpers.packageInstallationPath + self.packageName + "\\" + fileName

        for i in extensions:
            if i == self.scriptFile["fileType"]:
                if (self.parser.keyExists(self.scriptFile, "unzipPath")):
                    helpers.infoMessage(
                        "Unzipping  " + fileName + " to " + helpers.getToolsPath + "\\" + self.packageName)
                    extensions[i](zipFile, self.scriptFile["unzipPath"])
                    helpers.successMessage(
                        "Sucessfully unzipped " + fileName)
                else:
                    helpers.infoMessage(
                        "Unzipping  " + fileName + " to " + helpers.getToolsPath + "\\" + self.packageName)
                    extensions[i](zipFile, helpers.getToolsPath + "\\" + self.packageName)

                    helpers.successMessage(
                        "Sucessfully unzipped " + fileName)

    def checkHash(self):
        try:
            if json.Parser.keyExists(self.scriptFile, "downloadUrl64"):
                hashedKey = self.scriptFile["checksum64"]
            else:
                hashedKey = self.scriptFile["checksum"]

            check = hash.check(hashedKey, self.packageName, self.skipHashes)

            while check == True:
                return True
        except KeyError as e:
            pass

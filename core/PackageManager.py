import subprocess, sys, hashlib, helpers
from . import http
from . import FileManager as file
from . import JsonParser as json
from windows import winregistry
from . import hash


class Manager:
    def __init__(self):
        pass

    def installPackage(self, packageName, skipHashes=False):
        installable = {
            "exe": self.installExecutable,
            "msi": self.installExecutable,
            "unzip": self.unzipPackage
        }

        print(helpers.colors.fg.lightgrey + "Installing following packages:" + helpers.colors.reset)
        helpers.successMessage(packageName)
        print(
            helpers.colors.fg.lightgrey + "By installing you accept licenses for the packages." + helpers.colors.reset)

        self.agreement(self, packageName)
        self.isInstalled(packageName)
        self.getInstallationScript(self, packageName)
        self.downloadDependencies(packageName)
        self.checkHash(self, packageName, skipHashes)

        js = \
            json.Parser.fileToJson(json.Parser,
                                   helpers.packageInstallationPath + packageName + "\\" + packageName + ".cb")[
                "packageArgs"]
        for i in installable:
            if json.Parser.keyExists(js, i) or js["fileType"] == i:
                return installable[i](self, packageName)

    def removePackage(self, packageName):
        print(helpers.colors.fg.lightgrey + "Removing following packages:" + helpers.colors.reset)
        helpers.redColor(packageName)

        self.uninstallExecutable(packageName)
        self.cleanLeftOvers(packageName)
        helpers.successMessage("Successfully removed " + packageName)

    def getInstallationScript(self, packageName):
        packageWithExt = packageName + ".cb"
        try:
            if self.isInstalled(packageName):
                return helpers.packageInstallationPath + packageWithExt

            packageUrl = helpers.programList()[packageName]
            file.Manager.createFolder(helpers.packageInstallationPath + packageName)
            helpers.infoMessage("Downloading Installation Script of: " + packageWithExt)
            http.Http.download(http.Http, packageUrl,
                               helpers.packageInstallationPath + packageName + "\\" + packageWithExt, "")

        except KeyError as e:
            e = "This program does not exists on your list. Please update your lists with 'coban update' "
            helpers.errorMessage(e)
            exit()

    def isInstalled(packageName):
        packageWithExt = packageName + ".cb"
        packagePath = helpers.packageInstallationPath + packageName + "\\" + packageWithExt
        if file.Manager.fileExists(packagePath):
            helpers.infoMessage(
                "You already installed this package. You can upgrade it by 'coban upgrade " + packageName + "'")
            return False

    def installExecutable(self, packageName):
        parser = json.Parser
        packagePath = helpers.packageInstallationPath + packageName + "\\" + packageName
        loadJson = parser.fileToJson(parser, packagePath + ".cb")["packageArgs"]

        helpers.infoMessage(
            "Installing " + packageName + ". This will take a moment depends on software your installing. ")

        subprocess.call(packagePath + "." + loadJson["fileType"] + " " + loadJson["silentArgs"], shell=True)
        parser.addNewPackage(packageName)
        helpers.successMessage("Successfully installed " + packageName)

    def downloadDependencies(packageName):
        packagePathWithExt = helpers.packageInstallationPath + packageName + "\\" + packageName + ".cb"
        packagePathWithoutExt = helpers.packageInstallationPath + packageName + "\\" + packageName

        parser = json.Parser
        httpClass = http.Http

        loadJson = parser.fileToJson(parser, packagePathWithExt)["packageArgs"]
        if not file.Manager.fileExists(packagePathWithoutExt + "." + loadJson["fileType"]):
            if helpers.is_os_64bit():
                if parser.keyExists(loadJson, "downloadUrl64"):
                    helpers.infoMessage("Downloading " + packageName + " from: " + loadJson["downloadUrl64"])
                    httpClass.download(httpClass, loadJson["downloadUrl64"], packagePathWithoutExt,
                                       loadJson["fileType"])
            else:
                helpers.infoMessage("Downloading " + packageName + " from: " + loadJson["downloadUrl"])
                httpClass.download(httpClass, loadJson["downloadUrl"], packagePathWithoutExt, loadJson["fileType"])

    def uninstallExecutable(packageName):
        reg = winregistry.Registry
        package = reg.searchForSoftware(reg, packageName)

        packagePathWithExt = helpers.packageInstallationPath + packageName + "\\" + packageName + ".cb"
        parser = json.Parser
        js = parser.fileToJson(parser, packagePathWithExt)
        subprocess.call(package["UninstallString"] + " " + js["packageUninstallArgs"]["silentArgs"])
        parser.removePackage(packageName)

    def cleanLeftOvers(packageName):
        packagePath = helpers.packageInstallationPath + packageName
        fileManager = file.Manager
        fileManager.removeDir(fileManager, packagePath)

    def agreement(self, packageName):

        yes = {'yes', 'y', 'ye', ''}
        no = {'no', 'n'}

        choice = input("Do you want to install " + packageName + "? [Y/N]").lower()
        if choice in yes:
            return True
        elif choice in no:
            exit()
        else:
            sys.stdout.write("Please respond with 'yes' or 'no'")
            exit()

    def unzipPackage(self, packageName):
        extensions = {
            "7z": file.Manager.extract7z,
            "zip": file.Manager.extractZip
        }
        parser = json.Parser
        packagePathWithExt = helpers.packageInstallationPath + packageName + "\\" + packageName + ".cb"
        js = parser.fileToJson(parser, packagePathWithExt)["packageArgs"]
        fileName = packageName + "." + js["fileType"]
        zipFile = helpers.packageInstallationPath + packageName + "\\" + fileName

        for i in extensions:
            if i == js["fileType"]:
                if (parser.keyExists(js, "unzipPath")):
                    helpers.infoMessage(
                        "Unzipping  " + fileName + " to " + helpers.getToolsPath + "\\" + packageName)
                    extensions[i](zipFile, js["unzipPath"])
                    helpers.successMessage(
                        "Sucessfully unzipped " + fileName)
                else:
                    helpers.infoMessage(
                        "Unzipping  " + fileName + " to " + helpers.getToolsPath + "\\" + packageName)
                    extensions[i](zipFile, helpers.getToolsPath + "\\" + packageName)

                    helpers.successMessage(
                        "Sucessfully unzipped " + fileName)

    def checkHash(self, packageName, skipHashes):
        parser = json.Parser
        packagePathWithExt = helpers.packageInstallationPath + packageName + "\\" + packageName + ".cb"
        loadJson = parser.fileToJson(parser, packagePathWithExt)["packageArgs"]
        try:
            if json.Parser.keyExists(loadJson, "downloadUrl64"):
                hashedKey = loadJson["checksum64"]
            else:
                hashedKey = loadJson["checksum"]
        except KeyError as e:
            pass

        check = hash.check(hashedKey, packageName, skipHashes)

        while check == True:
            return True


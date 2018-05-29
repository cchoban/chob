from core import PackageManager
from core import JsonParser as json
import subprocess, helpers
from core import http
from core import FileManager as file
from Logger import Logger as log

class main(PackageManager.Manager):

    def isInstallable(self):

        self.installable = {
            "exe": self.installExecutable,
            "msi": self.installExecutable,
            "7z": self.unzipPackage,
            "zip": self.unzipPackage,
        }

        try:
            if self.scriptFile['fileType'] in self.installable:
                return True
            else:
                return False
        except Exception as e:
            log.new(e).logError()

    def installer(self):
            if self.agreement() == True:
                if not self.isInstalled():
                    self.getInstallationScript()
                    if self.isInstallable():
                        self.downloadDependencies()
                        self.checkHash()
                        self.beginAction()
                    else:
                        exit("This kind of package is not installable.")
                else:
                    helpers.alreadyInstalled(self.packageName)
            else:
                exit("You need to accept to contiune installation.")


    def getInstallationScript(self):
        try:
            if self.isInstalled():
                return self.packagePathWithExt

            packageUrl = helpers.programList()[self.packageName]
            file.Manager().createFolder(helpers.packageInstallationPath + self.packageName)
            helpers.infoMessage("Downloading Installation Script of: " + self.packageScriptName)
            #TODO: fix http self
            http.Http.download(http.Http, packageUrl,
                               helpers.packageInstallationPath + self.packageName + "\\" + self.packageScriptName, "")
            self.scriptFile = self.parser.fileToJson(self.packagePathWithExt)["packageArgs"]
        except KeyError as e:
            e = "This program does not exists on your list. Please update your lists with 'coban update' "
            helpers.errorMessage(e)
            exit()

    def downloadDependencies(self):
        httpClass = http.Http

        loadJson = self.scriptFile
        if not file.Manager().fileExists(self.packagePathWithoutExt + "." + loadJson["fileType"]):
            if helpers.is_os_64bit() and self.parser.keyExists(self.scriptFile, "downloadUrl64"):
                if self.parser.keyExists(loadJson, "downloadUrl64"):
                    helpers.infoMessage("Downloading " + self.packageName + " from: " + loadJson["downloadUrl64"])
                    httpClass.download(httpClass, loadJson["downloadUrl64"], self.packagePathWithoutExt,
                                       loadJson["fileType"])
            else:
                helpers.infoMessage("Downloading " + self.packageName + " from: " + loadJson["downloadUrl"])
                httpClass.download(httpClass, loadJson["downloadUrl"], self.packagePathWithoutExt, loadJson["fileType"])

    def unzipPackage(self):
        extensions = {
            "7z": file.Manager().extract7z,
            "zip": file.Manager().extractZip
        }

        fileName = self.packageName + "." + self.scriptFile["fileType"]
        zipFile = helpers.packageInstallationPath + self.packageName + "\\" + fileName

        for i in extensions:
            if i == self.scriptFile["fileType"]:
                if (self.parser.keyExists(self.scriptFile, "unzipPath")):
                    extensions[i](zipFile, self.scriptFile["unzipPath"])
                else:
                    extensions[i](zipFile, helpers.getToolsPath + "\\" + self.packageName)

    def installExecutable(self):
        helpers.infoMessage(
            "Installing " + self.packageName + ". This will take a moment depends on software your installing. ")
        print(self.packagePathWithoutExt + "." + self.scriptFile["fileType"] + " " + self.scriptFile["silentArgs"])
        subprocess.call(
            self.packagePathWithoutExt + "." + self.scriptFile["fileType"] + " " + self.scriptFile["silentArgs"],
            shell=True)
        self.parser.addNewPackage(self.packageName)
        helpers.successMessage("Successfully installed " + self.packageName)

    def beginAction(self):
        for i in self.installable:
            if json.Parser().keyExists(self.scriptFile, i) or self.scriptFile["fileType"] == i:
                return self.installable[i]()

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
                self.downloadScript()
                if self.isInstallable():
                    self.download()
                    self.checkHash()
                    if self.checkForDependencies():
                        self.downloadDependencies()
                    self.beginAction()
                else:
                    exit("This kind of package is not installable.")
            else:
                helpers.messages("info", "alreadyInstalled", self.packageName)
        else:
            exit("You need to accept to contiune installation.")

    def download(self):
        httpClass = http.Http

        loadJson = self.scriptFile

        if not file.Manager().fileExists(self.packagePathWithoutExt + "." + loadJson["fileType"]):
            if helpers.is_os_64bit() and self.parser.keyExists(self.scriptFile, "downloadUrl64"):
                # FIXME: wrong detection
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

        self.parser.addNewPackage(self.packageName, self.scriptFile["version"])

    def installExecutable(self):
        helpers.infoMessage(
            "Installing " + self.packageName + ". This will take a moment depends on software your installing. ")

        subprocess.call(
            self.packagePathWithoutExt + "." + self.scriptFile["fileType"] + " " + self.scriptFile["silentArgs"],
            shell=True)
        self.parser.addNewPackage(self.packageName, self.scriptFile["version"])
        helpers.successMessage("Successfully installed " + self.packageName)

    def beginAction(self):
        for i in self.installable:
            if json.Parser().keyExists(self.scriptFile, i) or self.scriptFile["fileType"] == i:
                return self.installable[i]()

    def checkForDependencies(self):
        if self.parser.keyExists(self.scriptFile, "dependencies"):
            for i in self.scriptFile["dependencies"]:
                if i in helpers.programList() and i not in helpers.installedApps()["installedApps"]:
                    helpers.infoMessage("Found dependencies: " + i)
                    self.oldPackageName = self.packageName
                    self.packageName = i
                    return True

    def downloadDependencies(self):
        downloadDependencies(self.packageName, self.skipHashes, self.forceInstallation, True).run()
        downloadDependencies(self.oldPackageName, self.skipHashes, self.forceInstallation, True).installPackage()

        try:
            super(main(self.oldPackageName, self.skipHashes, self.forceInstallation, True).installer())
        except Exception as e:
            log.new(e).logError()


class downloadDependencies(main):
    def run(self):
        try:
            installer = self.installer()
        except Exception as e:
            log.new(e).logError()

    def installPackage(self):
        try:
            self.packageName = self.oldPackageName
            installer = self.installer()
        except Exception as e:
            log.new(e).logError()

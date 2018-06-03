import helpers
from . import FileManager as file
from . import JsonParser as json
from . import hash


class Manager:
    def __init__(self, packageName, skipHashes, force, agreements):
        self.packageName = packageName
        self.oldPackageName = None
        self.skipHashes = skipHashes
        self.skipAgreements = agreements
        self.forceInstallation = force
        self.parser = json.Parser()

        if not isinstance(packageName, list):
            self.packagePathWithExt = helpers.packageInstallationPath + packageName + "\\" + packageName + ".cb"
            self.packagePathWithoutExt = helpers.packageInstallationPath + packageName + "\\" + packageName
            self.packageScriptName = self.packageName + ".cb"

            if file.Manager().fileExists(self.packagePathWithExt):
                if json.Parser(self.packagePathWithExt).isValid():
                    self.scriptFile = self.parser.fileToJson(self.packagePathWithExt)["packageArgs"]

    def installPackage(self):
        from .packageManager import installPackage as install

        for i in self.packageName:
            self.packageName = i
            self.packageScriptName = i + ".cb"

            install.main(i, self.skipHashes, self.forceInstallation, self.skipAgreements).installer()

    def removePackage(self):
        from .packageManager import removePackage as remove
        for i in self.packageName:
            self.packageName = i
            self.packageScriptName = i + ".cb"

            remove.main(i, self.skipHashes, self.forceInstallation, self.skipAgreements).uninstaller()

    def isInstalled(self):
        if self.parser.keyExists(helpers.installedApps()["installedApps"], self.packageName):
            return True
        else:
            return False

    def agreement(self, action="install"):
        if self.skipAgreements:
            return True

        yes = {'yes', 'y', 'ye', ''}
        no = {'no', 'n'}

        text = helpers.infoMessage("Do you want to " + action + " " + self.packageName + "? [Y/N]")
        print(text)
        choice = input("").lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            exit("Please respond with 'yes' or 'no'")

    def checkHash(self):
        try:
            if json.Parser().keyExists(self.scriptFile, "downloadUrl64"):
                hashedKey = self.scriptFile["checksum64"]
            else:
                hashedKey = self.scriptFile["checksum"]

            check = hash.check(hashedKey, self.packageName, self.skipHashes)

            while check == True:
                return True
        except KeyError as e:
            pass

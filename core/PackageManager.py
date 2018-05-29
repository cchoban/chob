import helpers
from . import FileManager as file
from . import JsonParser as json
from . import hash

class Manager:
    def __init__(self, packageName, skipHashes, force):
        self.packageName = packageName
        self.skipHashes = skipHashes
        self.forceInstallation = force
        self.packageScriptName = self.packageName + ".cb"
        self.packagePathWithExt = helpers.packageInstallationPath + packageName + "\\" + packageName + ".cb"
        self.packagePathWithoutExt = helpers.packageInstallationPath + packageName + "\\" + packageName

        self.parser = json.Parser()
        if file.Manager().fileExists(self.packagePathWithExt):
            self.scriptFile = self.parser.fileToJson(self.packagePathWithExt)["packageArgs"]

    def isInstalled(self):
        if self.parser.keyExists(helpers.installedApps()["installedApps"], self.packageName):
            return True
        else:
            return False

    def agreement(self, action="install"):

        yes = {'yes', 'y', 'ye', ''}
        no = {'no', 'n'}

        choice = input("Do you want to " + action + " " + self.packageName + "? [Y/N]").lower()
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


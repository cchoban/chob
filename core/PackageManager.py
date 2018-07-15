import helpers
from . import FileManager as file
from . import JsonParser as json
from . import hash
from .cli import cli
from sys import exit

class Manager:
    def __init__(self, packageName, skipHashes, force, agreements):
        self.packageName = packageName
        self.oldPackageName = None
        self.skipHashes = skipHashes
        self.skipAgreements = agreements
        self.forceInstallation = force
        self.parser = json.Parser()
        self.exit_code = None

        if not isinstance(packageName, list):
            self.packagePathWithoutExt = helpers.packageInstallationPath + \
                packageName + "\\" + packageName
            self.packagePathWithExt = self.packagePathWithoutExt + ".cb"
            self.packageScriptName = self.packageName + ".cb"

            if file.Manager().fileExists(self.packagePathWithExt):
                if json.Parser(self.packagePathWithExt).isValid():
                    self.scriptFile = self.parser.fileToJson(
                        self.packagePathWithExt)["packageArgs"]

    def installPackage(self):
        from .packageManager import installPackage as install
        for i in self.packageName:
            self.packageName = i
            self.packageScriptName = i + ".cb"

            install.main(i, self.skipHashes, self.forceInstallation,
                         self.skipAgreements).installer()

    def removePackage(self):
        self.uninstall = True
        from .packageManager import removePackage as remove
        for i in self.packageName:
            self.packageName = i
            self.packageScriptName = i + ".cb"

            remove.main(i, self.skipHashes, self.forceInstallation,
                        self.skipAgreements).uninstaller()

    def upgradePackage(self):
        from .packageManager import upgradePackage as upgrade
        for i in self.packageName:
            self.packageName = i
            self.packageScriptName = i + ".cb"

            upgrade.main(i, self.skipHashes, self.forceInstallation,
                         self.skipAgreements).run()

    def testPackage(self):
        from .packageManager import testPackage
        # install.main(self.packageName, self.skipHashes, self.forceInstallation, self.skipAgreements).testPackage()
        testPackage.main(self.packageName, self.skipHashes,
                         self.forceInstallation, self.skipAgreements).test()

    def isInstalled(self):
        if not self.forceInstallation and not helpers.isInstalled(self.packageName):
            return True
        else:
            return False

    def downloadScript(self, uninstall=False):
        try:
            self.scriptFile
            self.scriptFile["softwareName"]
        except AttributeError or KeyError as e:
            cli.main().downloadScript(self.packageName)
            if not uninstall:
                self.scriptFile = self.parser.fileToJson(
                    self.packagePathWithExt)["packageArgs"]
            else:
                self.scriptFile = self.parser.fileToJson(
                    self.packagePathWithExt)
                print(self.scriptFile)

    def agreement(self, action="install"):
        if self.skipAgreements:
            return True

        yes = {'yes', 'y', 'ye', ''}
        no = {'no', 'n'}

        text = helpers.infoMessage(
            "Do you want to " + action + " " + self.packageName + "? [Y/N]")
        print(text)
        choice = input("").lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            exit("Please respond with 'yes' or 'no'")

    def checkHash(self, sandboxed=False):
        try:
            if json.Parser().keyExists(self.scriptFile, "downloadUrl64"):
                hashedKey = self.scriptFile["checksum64"]
            else:
                hashedKey = self.scriptFile["checksum"]

            check = hash.check(hashedKey, self.packageName,
                               self.skipHashes, sandboxed)

            while check == True:
                return True
        except KeyError as e:
            pass

    def valid_exit_code(self):
        if self.exit_code in self.scriptFile["validExitCodes"] or str(self.exit_code) in self.scriptFile["validExitCodes"]:
            return True
        else:
            return False

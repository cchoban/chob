from core import PackageManager, FileManager
import helpers, subprocess
from windows import winregistry
from Logger import Logger as log
from ..cli.cli import main as cli

class main(PackageManager.Manager):

    def uninstaller(self):
        if self.isInstalled():
            if self.agreement("uninstall"):
                self.uninstallExecutable()
                self.uninstallFromTools()
        else:
            helpers.infoMessage("There is no packages with name of " + self.packageName)
            exit()

    def uninstallExecutable(self):
        reg = winregistry.Registry()
        package = reg.searchForSoftware(self.packageName)
        if package == None:
            package = reg.searchForSoftware64(self.packageName)

        try:
            self.scriptFile
        except AttributeError as e:
            cli().downloadScript(self.packageName)


        self.scriptFile = self.parser.fileToJson(self.packagePathWithExt)
        if package:
            try:
                helpers.infoMessage("Trying to remove " + self.packageName + " with original uninstaller..")
                subprocess.call(
                    package["UninstallString"] + " " + self.scriptFile["packageUninstallArgs"]["silentArgs"])
                helpers.successMessage("Successfully removed: " + self.packageName)

            except KeyError or Exception as e:
                log.new(e).logError()
            self.parser.removePackage(self.packageName)
        else:
            helpers.infoMessage("Skipping uninstaller process - No registry key found.")
            helpers.infoMessage("Cleanup left overs..")
            FileManager.Manager().cleanup(self.packageName)
            self.parser.removePackage(self.packageName)

    def uninstallFromTools(self):
        file = FileManager.Manager()
        path = helpers.getToolsPath
        if file.fileExists(path + "\\" + self.packageName):
            file.removeDir(file.fileExists(path + "\\" + self.packageName))
        else:
            return False

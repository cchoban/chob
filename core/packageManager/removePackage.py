from core import PackageManager, FileManager
import helpers, subprocess
from windows import winregistry
from Logger import Logger as log
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
        reg = winregistry.Registry
        package = reg.searchForSoftware(reg, self.packageName)

        if package:
            try:
                helpers.infoMessage("Trying to remove "+self.packageName+" with original uninstaller..")
                subprocess.call(
                    package["UninstallString"] + " " + self.scriptFile["packageUninstallArgs"]["silentArgs"])
                helpers.successMessage("Successfully removed: " + self.packageName)

            except KeyError or Exception as e:
                log.new(e).logError()
            self.parser.removePackage()
        else:
            helpers.infoMessage("Skipping uninstaller process - No registry key found.")
            helpers.infoMessage("Cleanup left overs..")
            self.parser.removePackage(self.packageName)


    def uninstallFromTools(self):
        file = FileManager.Manager()
        path = helpers.getToolsPath
        if file.fileExists(path+"\\"+self.packageName):
            print("toolsda mevcut ")
        else:
            print("toolsda mevcut deil")

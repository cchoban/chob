from core import PackageManager, FileManager
import helpers
from subprocess import call as callExe
from windows import winregistry
from Logger import Logger as log


class main(PackageManager.Manager):

    def uninstaller(self):
        if self.isInstalled():
            if self.agreement("uninstall"):
                self.downloadScript()
                if not self.__findReg() == False:
                    self.uninstallExecutable()
                self.uninstallFromTools()
        else:
            helpers.infoMessage("There is no packages with name of " + self.packageName)
            exit()

    def __findReg(self):
        reg = winregistry.Registry()
        package = reg.searchForSoftware(self.scriptFile["softwareName"])

        if package == None:
            package = reg.searchForSoftware64(self.scriptFile["softwareName"])

        if package:
            return package
        else:
            helpers.infoMessage("Skipping uninstaller process - No registry key found.")
            helpers.infoMessage("Cleanup left overs..")
            FileManager.Manager().cleanup(self.packageName)
            self.parser.removePackage(self.packageName)
            return False

    def uninstallExecutable(self):
        package = self.__findReg()
        try:
            helpers.infoMessage("Trying to remove {0} with original uninstaller..".format(self.packageName))
            callExe(
                "{0} {1}".format(package["UninstallString"], self.scriptFile["packageUninstallArgs"]["silentArgs"]))
            helpers.successMessage("Successfully removed: " + self.packageName)
            self.parser.removePackage(self.packageName)

        except KeyError or Exception as e:
            log.new(e).logError()
        self.parser.removePackage(self.packageName)


    def uninstallFromTools(self):
        file = FileManager.Manager()
        path = helpers.getToolsPath
        if file.fileExists(path + "\\" + self.packageName):
            file.removeDir(path + "\\" + self.packageName)
        else:
            return False

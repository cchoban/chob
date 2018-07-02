from core import PackageManager, FileManager
import helpers
from subprocess import call as callExe
from windows import winregistry
from Logger import Logger as log


class main(PackageManager.Manager):

    def uninstaller(self):
        if self.isInstalled():
            if self.agreement("uninstall"):
                if not FileManager.Manager().fileExists(self.packagePathWithExt):
                    self.downloadScript()
                if self.__findReg():
                    self.uninstallExecutable()
                self.uninstallFromTools()
                self.__remove_symlinks()
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
            self.__do_cleanup()
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


    def __remove_symlinks(self):
        file = FileManager.Manager()
        symlinks = helpers.symlinkList()
        if self.packageName in symlinks:
            path = FileManager.Manager().os().path.join(symlinks[self.packageName])
            unlink = file.os().unlink(path)
            self.parser.remove_package_symlink(self.packageName)

    def uninstallFromTools(self):
        helpers.infoMessage("Removing {0} from tools folder".format(self.packageName))
        file = FileManager.Manager()
        path = helpers.getToolsPath + "\\" + self.packageName
        if file.fileExists(path):
            file.removeDir(path)
            helpers.successMessage("Successfully removed "+self.packageName)
        else:
            return False

    def __do_cleanup(self):
        helpers.infoMessage("Skipping uninstaller process - No registry key found.")
        helpers.infoMessage("Cleanup left overs..")
        FileManager.Manager().cleanup(self.packageName)
        self.parser.removePackage(self.packageName)
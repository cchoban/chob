from core import PackageManager, FileManager
import helpers
from subprocess import Popen
from windows import winregistry
from Logger import Logger as log
from sys import exit

class main(PackageManager.Manager):
    def uninstaller(self):
        if self.isInstalled():
            if self.agreement("uninstall"):
                if not FileManager.Manager().fileExists(self.packagePathWithExt):
                    self.downloadScript(True)
                else:
                    self.scriptFile = self.parser.fileToJson(self.packagePathWithExt)

                self.checkForDependencies()

                if self.__findReg():
                    self.uninstallExecutable()
                else:
                    self.uninstallFromTools()
                self.__remove_symlinks()

                self.remove_dependencies()
        else:
            helpers.infoMessage("There is no packages with name of " + self.packageName)
            return False


    def __findReg(self):
        reg = winregistry.Registry()
        package = reg.searchForSoftware(self.scriptFile["packageArgs"]["softwareName"])

        if package == None:
            package = reg.searchForSoftware64(self.scriptFile["packageArgs"]["softwareName"])

        if package:
            return package
        else:
            self.__do_cleanup()
            return False

    def uninstallExecutable(self):
        package = self.__findReg()
        try:
            if package:
                helpers.infoMessage("Trying to remove {0} with original uninstaller..".format(self.packageName))

                try:
                    call_exe = Popen('{0} {1}'.format(package["UninstallString"], self.scriptFile["packageUninstallArgs"]["silentArgs"]))
                except OSError as e:
                    if e.errno == 193:
                        call_exe = Popen('{0} {1}'.format(package["UninstallString"], self.scriptFile["packageUninstallArgs"]["silentArgs"]), shell=True)


                call_exe.communicate()[0]
                self.exit_code = call_exe.returncode
                self.scriptFile = self.parser.fileToJson(self.packagePathWithExt)["packageArgs"]

                if self.valid_exit_code():
                    helpers.successMessage("Successfully removed: " + self.packageName)
                    self.parser.removePackage(self.packageName)
                else:
                    helpers.errorMessage("Uninstall process was not succeed.")

        except KeyError or Exception as e:
            log.new(e).logError()


    def __remove_symlinks(self):
        fs = FileManager.Manager()
        symlinks = helpers.symlinkList()
        if self.packageName in symlinks:
            for file in symlinks[self.packageName]:
                fileDest = fs.os().path.join(helpers.getCobanBinFolder, file)
                unlink = fs.os().unlink(fileDest)
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

    def remove_dependencies(self):
        if self.dependencies:
            installedApps = helpers.installedApps()['installedApps']
            for i in installedApps:
                if installedApps[i].get('dependencies'):
                    if self.dependencies in installedApps[i].get('dependencies'):
                        helpers.errorMessage('Skipping uninstalling "{}" as it uses by another package:  "{}"'.format(self.dependencies, i))
                        return False

            dependencies = self.dependencies if not isinstance(self.dependencies, list) else [i for i in self.dependencies]
            self.packageName = dependencies
            self.removePackage()

    def __do_cleanup(self):
        helpers.infoMessage("Skipping uninstaller process - No registry key found.")
        helpers.infoMessage("Cleanup left overs..")
        FileManager.Manager().cleanup(self.packageName)
        self.parser.removePackage(self.packageName)

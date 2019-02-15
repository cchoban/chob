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
                if not FileManager.Manager().fileExists(
                        self.packagePathWithExt):
                    self.downloadScript(True)
                else:
                    self.scriptFile = self.parser.fileToJson(
                        self.packagePathWithExt)

                self.checkForDependencies()

                if self.__findReg():
                    self.uninstallExecutable()
                else:
                    self.uninstallFromTools()
                    self.remove_environments()
                    self.remove_from_path_env()
                self.__remove_symlinks()

                self.printNotesFromParser()

                self.remove_dependencies()

        else:
            helpers.infoMessage("There is no packages with name of " +
                                self.packageName)
            return False

    def __findReg(self):
        reg = winregistry.Registry()
        package = reg.searchForSoftware(
            self.scriptFile["packageArgs"]["softwareName"])

        if package:
            return package
        else:
            self.__do_cleanup()
            return False

    def uninstallExecutable(self):
        package = self.__findReg()
        try:
            if package:
                helpers.infoMessage(
                    "Trying to remove {0} with original uninstaller..".format(
                        self.packageName))

                try:
                    call_exe = Popen('{0} {1}'.format(
                        package["UninstallString"],
                        self.scriptFile["packageUninstallArgs"]["silentArgs"]))
                except OSError as e:
                    if e.errno == 193:
                        call_exe = Popen(
                            '{0} {1}'.format(
                                package["UninstallString"],
                                self.scriptFile["packageUninstallArgs"]
                                ["silentArgs"]),
                            shell=True)

                call_exe.communicate()[0]
                self.exit_code = call_exe.returncode
                self.scriptFile = self.parser.fileToJson(
                    self.packagePathWithExt)["packageArgs"]

                if self.valid_exit_code():
                    FileManager.Manager().cleanup(self.packageName)
                    self.parser.removePackage(self.packageName)

                    helpers.successMessage("Successfully removed: " +
                                           self.packageName)

                else:
                    helpers.errorMessage("Uninstall process was not succeed.")

        except KeyError or Exception as e:
            log.new(e).logError()

    def __remove_symlinks(self):
        fs = FileManager.Manager()
        symlinks = helpers.symlinkList()
        if self.packageName in symlinks:
            for file in symlinks[self.packageName] if isinstance(
                    symlinks[self.packageName], list) else []:
                fileDest = fs.os().path.join(helpers.getCobanBinFolder, file)
                unlink = fs.os().unlink(fileDest)
            self.parser.remove_package_symlink(self.packageName)

    def remove_environments(self):
        from windows import winhelpers
        self.scriptFile = self.scriptFile.get('packageArgs') or self.scriptFile

        try:
            if self.parser.keyExists(self.scriptFile, 'environments'):
                for env in self.scriptFile['environments']:
                    winhelpers.remove_env(env)
            else:
                return True
        except Exception as e:
            print(e)

    def remove_from_path_env(self):
        from windows import winhelpers
        self.scriptFile = self.scriptFile.get('packageArgs') or self.scriptFile

        try:
            if self.parser.keyExists(self.scriptFile, 'path_env'):
                for path in self.scriptFile.get('path_env'):
                    winhelpers.remove_from_path(path)
            else:
                return True
        except Exception as e:
            print(e)

    def uninstallFromTools(self):
        helpers.infoMessage("Removing {0} from tools folder".format(
            self.packageName))
        file = FileManager.Manager()
        path = helpers.getToolsPath + "\\" + self.packageName
        if file.fileExists(path):
            file.removeDir(path)
            helpers.successMessage("Successfully removed " + self.packageName)
        else:
            return False

    def remove_dependencies(self):
        if self.dependencies:
            installedApps = helpers.installedApps()['installedApps']
            for i in installedApps:
                if installedApps[i].get('dependencies'):
                    #FIXME: potential problems
                    if self.dependencies == installedApps[i].get(
                            'dependencies'):
                        helpers.errorMessage(
                            'Skipping uninstalling "{}" as it uses by another package:  "{}"'
                            .format(self.dependencies, i))
                        return False

            dependencies = self.dependencies if not isinstance(
                self.dependencies, list) else [i for i in self.dependencies]
            self.packageName = dependencies
            self.removePackage()

    def __do_cleanup(self):
        helpers.infoMessage(
            "Skipping uninstaller process - No registry key found.")
        helpers.infoMessage("Cleanup left overs..")
        FileManager.Manager().cleanup(self.packageName)
        self.parser.removePackage(self.packageName)

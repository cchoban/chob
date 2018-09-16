from core import PackageManager
from core import JsonParser as json
import subprocess
import helpers
from core import http
from core import FileManager as file
from Logger import Logger as log
from sys import exit

class main(PackageManager.Manager):
    def isInstallable(self):

        self.installable = {
            "exe": self.installExecutable,
            "msi": self.installExecutable,
            "7z": self.unzipPackage,
            "zip": self.unzipPackage,
            'tar': self.unzipPackage,
            'tar.xz': self.unzipPackage
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
                    self.checkForDependencies()
                    self.beginAction()
                    if not self.parser.keyExists(self.scriptFile, "unzip"):
                        if self.valid_exit_code():
                            self.parser.addNewPackage(self.packageName, {"version":self.scriptFile['version'], 'dependencies': self.dependencies})
                            helpers.successMessage("Successfully installed "+ self.packageName)
                            self.downloadDependencies()
                            return True
                        else:
                            helpers.errorMessage("{0} returned was not installed successfully.".format(self.packageName))
                            if helpers.is_verbose():
                                helpers.errorMessage('{} returned {} exit code.'.format(self.packageName, self.exit_code))
                            return False
                    else:
                        helpers.successMessage("Successfully installed "+self.packageName)
                        self.downloadDependencies()
                        return True
                else:
                    exit(
                        "This file type is not supported. Create issue if you really think it should."
                    )
            else:
                helpers.messages("info", "alreadyInstalled", self.packageName)
        else:
            exit("You need to accept to contiune installation.")

    def download(self):
        httpClass = http.Http()
        loadJson = self.scriptFile
        download_url = loadJson["downloadUrl64"] if helpers.is_os_64bit() and self.parser.keyExists(self.scriptFile, "downloadUrl64") else loadJson["downloadUrl"]
        download_path = self.packagePathWithoutExt
        file_path = download_path+"."+loadJson["fileType"]
        self.install_path = file_path

        if not file.Manager().fileExists(file_path):

            if self.parser.keyExists(self.scriptFile, "64bitonly"):
                if not helpers.is_os_64bit():
                    helpers.errorMessage("This package is only for 64-bit devices.")
                    exit()
                else:
                    helpers.infoMessage("Downloading " + self.packageName +
                                        " from: " + loadJson["downloadUrl64"])
                    httpClass.download(loadJson["downloadUrl64"],
                                       download_path,
                                       loadJson["fileType"])
                    return True

            helpers.infoMessage("Downloading " + self.packageName +
                                " from: " + download_url)
            httpClass.download(download_url,
                                download_path,
                                loadJson["fileType"])

    def unzipPackage(self):
        extensions = {
            "7z": file.Manager().extract7z,
            "zip": file.Manager().extractZip,
            'tar': file.Manager().extract7z,
            'tar.xz': file.Manager().extract7z
        }

        fileName = self.packageName + "." + self.scriptFile["fileType"]

        #TODO: add verbose mode here
        zipFile = helpers.packageInstallationPath + self.packageName + "\\" + fileName

        for i in extensions:
            if i == self.scriptFile["fileType"]:
                if (self.parser.keyExists(self.scriptFile, "unzipPath")):
                    extensions[i](zipFile, self.scriptFile["unzipPath"])
                else:
                    extensions[i](zipFile,helpers.getToolsPath + "\\" + self.packageName)

                if (self.parser.keyExists(self.scriptFile, "createShortcut")):
                    self.__create_shorcut()
            self.parser.addNewPackage(self.packageName, {"version":self.scriptFile['version'], 'dependencies': self.dependencies})

    def __create_shorcut(self):
        bit_64 = self.scriptFile['createShortcut'].get('64bit')
        bit_32 = self.scriptFile['createShortcut'].get('32bit')
        files = []
        binFolder = helpers.getCobanBinFolder + '{}'
        ask = helpers.askQuestion(
            "Do you want to create link {0} to lib folder ( This will help you to launch app from command prompt)".
            format(self.packageName))

        if ask:
            helpers.infoMessage("Creating shortcut for " + self.packageName)
            if helpers.is_os_64bit() and bit_64:
                for exeName in bit_64:
                    if not file.Manager().fileExists(binFolder.format(exeName)):
                        extract_filename = exeName.split('\\')[-1]
                        createSymLink = file.Manager().createSymLink(self.packageName, exeName)
                        files.append(self.packageName + '.ps1')

            if helpers.is_os_64bit() and not bit_64:
                for exeName in bit_32:
                    if not file.Manager().fileExists(binFolder.format(exeName)):
                        extract_filename = exeName.split('\\')[-1]
                        createSymLink = file.Manager().createSymLink(self.packageName, exeName)
                        files.append(self.packageName + '.ps1')

            if not helpers.is_os_64bit() and bit_32:
                for exeName in bit_32:
                    if not file.Manager().fileExists(binFolder.format(exeName)):
                        extract_filename = exeName.split('\\')[-1]
                        createSymLink = file.Manager().createSymLink(self.packageName, exeName)
                        files.append(self.packageName+'.ps1')

            #TODO: add enviroments to creator
            #TODO: add enviroments key to uninstall args for deleting envs later.
            #TODO: add post_install package args
            #TODO: add run_from_tools package args
            self.set_envs()
            self.add_to_path_env()



            json.Parser().add_new_symlink(self.packageName, files)
            helpers.successMessage("Successfully created shortcut(s)")

    def installExecutable(self):
        helpers.infoMessage(
            "Installing " + self.packageName +". This will take a moment depends on software your installing. ")
        if self.parser.keyExists(self.scriptFile, "64bitonly"):
            if not helpers.is_os_64bit():
                helpers.errorMessage("This package is only for 64-bit devices.")
                return False
        try:
            call_exe = subprocess.Popen('"{0}" {1}'.format(self.install_path,self.scriptFile["silentArgs"]))
        except OSError as e:
            if e.winerror == 193:
                call_exe = subprocess.Popen('"{0}" {1}'.format(self.install_path,self.scriptFile["silentArgs"]), shell=True)
        call_exe.communicate()[0]
        self.exit_code = call_exe.returncode

    def beginAction(self):
        for i in self.installable:
            if json.Parser().keyExists(self.scriptFile,i) or self.scriptFile["fileType"] == i:
                return self.installable[i]()

    def downloadDependencies(self):
        self.packageName = self.dependencies
        self.installPackage()

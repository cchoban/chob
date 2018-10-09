import os
import helpers
import zipfile
from shutil import rmtree, move, copy
from Logger import Logger
from subprocess import run, call, DEVNULL
from Logger import Logger as log
from json import dumps
from sys import exit

class Manager:
    def os(self):
        """
        OS

        :return object
        """

        return os

    def fileExists(self, path=""):
        """
        Checks if file is exists.
        :param path:
        :return bool:
        """
        try:
            if os.path.exists(path):
                return True
            else:
                return False
        except FileNotFoundError as e:
            log.new(e).logError()
            if helpers.is_verbose():
                helpers.errorMessage("FileManager.fileExists - File not found: "+str(e))
            exit()
    def createFolder(self, path, hidden=False):
        """
        Creates folder with specified path
        :param path:
        """
        try:
            if not os.path.exists(path):
                os.makedirs(path)
                if hidden:
                    call(["attrib", "+H", os.path.abspath(path)])
        except Exception as e:
            log.new(e).logError()
            if helpers.is_verbose():
                helpers.errorMessage("FileManager.createFolder - "+str(e))
            exit()
    def createFile(self, path, content="", hidden=False):
        """
        Creates file with content
        :param path:
        :param content:
        """
        try:
            if not os.path.exists(path):
                with open(path, "w") as f:
                    f.write(content)
                    f.close()

                if hidden:
                    call(["attrib", "+H", os.path.abspath(path)])
        except Exception as e:
            log.new(e).logError()
            if helpers.is_verbose():
                helpers.errorMessage("FileManager.createFile - "+str(e))

    def deleteFile(self, path):
        """
        Deletes file
        :param path: Path to file
        """
        try:
            if os.path.exists(path):
                if os.path.isdir(path):
                    rmtree(path)
                    os.remove(path)
                else:
                    os.remove(path)
        except Exception as e:
            log.new(e).logError()
            if helpers.is_verbose():
                helpers.errorMessage("FileManager.deleteFile - " + str(e))

    def createSymLink(self, package_name, shortcut_name, executable):
        """
        Creates symlink
        :param packageName: Name of package
        :param executable: Executable file of package to create executable powershell script
        """
        try:
            dest = helpers.getCobanBinFolder + '\\{}.ps1'.format(shortcut_name)
            if not self.fileExists(dest):
                with open(helpers.getCobanPath+'\\whof.ps1', 'r') as f:
                    content = f.read()

                    if '{packageExecutable}' in content:
                        content = content.replace('{packageExecutable}', '{}\{}'.format(package_name, executable))
                        with open(dest, 'w') as f:
                            f.write(content)
                            f.close()
                    f.close()
            else:
                return False
        except Exception as e:
            log.new(e).logError()
            if helpers.is_verbose():
                helpers.errorMessage(
                    "FileManager.createSymlink: " + str(e))
            return False


    def createJsonFile(self, path, withDict={}):
        """
        Creates json file with help of createFile function
        :param path:
        :param withDict:
        """
        try:
            self.createFile(dumps(withDict))
        except FileNotFoundError or PermissionError or Exception as e:
            log.new(e).logError()
            if helpers.is_verbose():
                helpers.errorMessage("FileManager.createJsonFile: "+str(e.strerror))

    def removeDir(self, path):
        """
        Removes dir
        :param path:
        """
        if self.fileExists(path):
            try:
                rmtree(path)
                os.removedirs(path)
            except FileNotFoundError or WindowsError or PermissionError or Exception as e:
                log.new(e).logError()
                if helpers.is_verbose():
                    helpers.errorMessage("FileManager.removeDir: "+str(e.strerror))
        else:
            helpers.infoMessage(
                "Path does not exists while trying to remove it: " + path)

    def moveFile(self, filePath, fileDest):
        """
        Moves file to specific directory.
        :param filePath: File to be moved from.
        :param fileDest: File to be moved to.
        """
        if self.fileExists(filePath.replace('*','')):
            try:
                if filePath.endswith('*'):
                    filePath = filePath.replace('*', '')
                    for i in os.listdir(filePath):
                        move(os.path.join(filePath, i), fileDest)
                else:
                    move(filePath, fileDest)
            except WindowsError or FileNotFoundError or FileExistsError as e:
                log.new(e).logError()
                if helpers.is_verbose():
                    helpers.errorMessage("FileManager.moveFile: "+str(e.strerror))
                    exit()

    def copyFile(self, filePath, fileDest):
        """
        Copys file to specific directory.
        :param filePath: File to be copied from.
        :param fileDest: File to be copied to.
        """

        if self.fileExists(filePath):
            try:
                copy(filePath, fileDest)
            except WindowsError or FileNotFoundError or FileExistsError as e:
                log.new(e).logError()
                if helpers.is_verbose():
                    helpers.errorMessage("FileManager.copyFile: "+str(e.strerror))
                exit()


    def __zipdir(self, path, zip, ignoreFiles=[]):
        for file in os.listdir(path):
            if not file in ignoreFiles:
                if os.path.isfile(file):
                    zip.write(file)

                if os.path.isdir(file):
                    for oss in os.listdir(os.path.join(path, file)):
                        zip.write(file+"\\"+oss)

    def makeZip(self, path, zipName, ignoreFiles=[]):
        """
        Creates a zip file.
        :param path: Path where you want your zip file to be saved.
        :param zipName: Name you zip.
        :param ignoreFiles: Ignore specific files.
        """
        try:
            zf = zipfile.ZipFile(path + "\\" + zipName,
                                 "w", zipfile.ZIP_DEFLATED)
            if len(os.listdir(path)) > 1:
                self.__zipdir(path, zf, ignoreFiles)
            else:
                zf.write(path)
                zf.close()

            return True
        except OSError or PermissionError or FileNotFoundError as e:
            log.new(e).logError()
            if helpers.is_verbose():
                helpers.errorMessage("FileManager.makeZip: "+str(e.strerror))
            exit()


    def extractZip(self, zip, dest, extractFolder):
        from tempfile import gettempdir
        from uuid import uuid4

        """
        Extract zip
        :param zip: Zip file path
        :param dest: Path to be extracted
        :param extractFolder: Folder to be extracted inside zip file.
        """
        try:
            __rand = uuid4().hex.upper()[0:6]
            tmp_file = gettempdir()+"\\"+__rand
            helpers.infoMessage("Unzipping " + zip + " to " + dest)

            zf = zipfile.ZipFile(zip, "r")
            if extractFolder:
                zf.extractall(tmp_file)
                self.moveFile(tmp_file+"\\"+extractFolder, dest)
            else:
                zf.extractall(dest)

            zf.close()
            helpers.successMessage(
                "Successfully unzipped " + zip + " to " + dest)
        except WindowsError or PermissionError or FileNotFoundError as e:
            log.new(e).logError()
            if helpers.is_verbose():
                helpers.errorMessage("FileManager.extractZip: "+str(e.strerror))
            exit()

    def extract7z(self, zip, dest, extractFolder):
        from tempfile import gettempdir
        from uuid import uuid4
        """
        Extract 7zip
        :param zip: Zip file path
        :param dest: Path to be extracted
        :param extractFolder: Folder to be extracted inside zip file.
        """

        try:
            __rand = uuid4().hex.upper()[0:6]
            tmp_file = gettempdir()+"\\"+__rand
            helpers.infoMessage("Unzipping " + zip + " to " + dest)

            if extractFolder:
                processArgs = helpers.getCobanBinFolder + \
                    "7za.exe x -o{0} -y {1}".format(tmp_file, zip)
            else:
                processArgs = helpers.getCobanBinFolder + \
                    "7za.exe x -o{0} -y {1}".format(dest, zip)

            runProcess = run(processArgs, stderr=DEVNULL,
                             stdout=DEVNULL)

            if self.fileExists(tmp_file) and len(os.listdir(tmp_file)) > 0:
                if zip.endswith('.tar.gz') or zip.endswith('.tar.xz'):
                    for i in os.listdir(tmp_file):
                        if i.endswith('.tar'):
                            runProcess = run(
                                "7za.exe x -o{0} -y {1}".format(tmp_file, os.path.abspath(os.path.join(tmp_file, i))), stderr=DEVNULL,
                                stdout=DEVNULL)

            if extractFolder:
                self.moveFile(os.path.join(tmp_file, extractFolder), dest)

            helpers.successMessage(
                "Successfully unzipped " + zip + " to " + dest)
        except Exception as e:
            log.new(e).logError()
            if helpers.is_verbose():
                helpers.errorMessage("FileManager.extract7z: "+str(e))
            exit()


    def cleanup(self, packageName=""):
        """
        Removing unused meta-data packages.
        :param packageName:
        """
        packagesPath = helpers.getCobanPath + "\\packages\\" + packageName

        if packageName != "":
            return self.removeDir(packagesPath)

        for i in helpers.installedApps()["installedApps"]:
            path = packagesPath + i
            if self.fileExists(path):
                self.removeDir(path)
                helpers.successMessage("Removed: " + i)

        for i in os.listdir(packagesPath):
            path = packagesPath + i
            if not i in helpers.installedApps()["installedApps"]:
                self.removeDir(path)
                helpers.successMessage("Removed: " + i)

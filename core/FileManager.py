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

    def createSymLink(self, path, dest):
        from  win32file import CreateSymbolicLink
        """
        Creates symlink
        :param path: path to file you want to create symlink
        :param dest: path to save symlinked file
        """
        try:
            CreateSymbolicLink(dest, path, 0)
            return True
        except OSError or PermissionError or WindowsError or FileNotFoundError or FileExistsError as e:
            log.new(e).logError()
            if helpers.is_verbose():
                helpers.errorMessage("FileManager.createSymlink: "+str(e.strerror))
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
        :param filePath:
        :param fileDest:
        """

        if self.fileExists(filePath):
            try:
                move(filePath, fileDest)
            except WindowsError or FileNotFoundError or FileExistsError as e:
                log.new(e).logError()
            if helpers.is_verbose():
                helpers.errorMessage("FileManager.moveFile: "+str(e.strerror))
                exit()

    def copyFile(self, filePath, fileDest):
        """
        Copys file to specific directory.
        :param filePath:
        :param fileDest:
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
    def extractZip(self, zip, dest):
        """
        Extract zip
        :param zip:
        :param dest:
        """
        try:
            helpers.infoMessage("Unzipping " + zip + " to " + dest)
            zf = zipfile.ZipFile(zip, "r")
            zf.extractall(dest)
            zf.close()
            helpers.successMessage(
                "Successfully unzipped " + zip + " to " + dest)
        except WindowsError or PermissionError or FileNotFoundError as e:
            log.new(e).logError()
            if helpers.is_verbose():
                helpers.errorMessage("FileManager.extractZip: "+str(e.strerror))
            exit()
    def extract7z(self, zip, dest):
        """
        Extract 7zip
        :param zip:
        :param dest:
        """
        try:
            processArgs = helpers.getCobanBinFolder + \
                "7za.exe x -o{0} -y {1}".format(dest, zip)
            helpers.infoMessage("Unzipping " + zip + " to " + dest)
            runProcess = run(processArgs, stderr=DEVNULL,
                             stdout=DEVNULL, shell=True)
            helpers.successMessage(
                "Successfully unzipped " + zip + " to " + dest)
        except WindowsError or PermissionError or FileNotFoundError as e:
            log.new(e).logError()
            if helpers.is_verbose():
                helpers.errorMessage("FileManager.extract7z: "+str(e.strerror))
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
            print(path)
            if self.fileExists(path):
                self.removeDir(path)
                helpers.successMessage("Removed: " + i)

        for i in os.listdir(packagesPath):
            path = packagesPath + i
            if not i in helpers.installedApps()["installedApps"]:
                self.removeDir(path)
                helpers.successMessage("Removed: " + i)

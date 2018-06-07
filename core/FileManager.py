import os, helpers, zipfile
from shutil import rmtree
from Logger import Logger
from subprocess import run, DEVNULL
from Logger import Logger as log
from json import dumps


class Manager:
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
            exit()

    def createFolder(self, path):
        """
        Creates folder with specified path
        :param path:
        """
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except Exception as e:
            exit()

    def createFile(self, path, content=""):
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
        except Exception as e:
            log.new(e).logError()

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
        else:
            helpers.infoMessage("Path does not exists while trying to remove it: " + path)

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
            helpers.successMessage("Successfully unzipped " + zip + " to " + dest)
        except WindowsError or PermissionError or FileNotFoundError as e:
            Logger.new(e).logError()
            exit()

    def extract7z(self, zip, dest):
        """
        Extract 7zip
        :param zip:
        :param dest:
        """
        try:
            processArgs = helpers.getCobanBinFolder + "7za.exe x -o{0} -y {1}".format(dest, zip)
            helpers.infoMessage("Unzipping " + zip + " to " + dest)
            runProcess = run(processArgs, stderr=DEVNULL, stdout=DEVNULL, shell=True)
            helpers.successMessage("Successfully unzipped " + zip + " to " + dest)
        except WindowsError or PermissionError or FileNotFoundError as e:
            Logger.new(e).logError()
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

import os, helpers, zipfile
from shutil import rmtree
from Logger import Logger
from subprocess import run, DEVNULL
from Logger import Logger as log
from json import dumps


class Manager:
    def fileExists(self, path=""):
        try:
            if os.path.exists(path):
                return True
            else:
                return False
        except FileNotFoundError as e:
            exit()

    def createFolder(self, path):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except Exception as e:
            exit()

    def createFile(self, path, content=""):
        try:
            if not os.path.exists(path):
                with open(path, "w") as f:
                    f.write(content)
                    f.close()
        except Exception as e:
            log.new(e).logError()

    def createJsonFile(self, path, withDict={}):
        try:
            self.createFile(dumps(withDict))
        except FileNotFoundError or PermissionError or Exception as e:
            log.new(e).logError()

    def removeDir(self, path):
        if self.fileExists(path):
            try:
                rmtree(path)
                os.removedirs(path)
            except FileNotFoundError or WindowsError or PermissionError or Exception as e:
                log.new(e).logError()
        else:
            helpers.infoMessage("Path does not exists while trying to remove it: " + path, True)

    def extractZip(self, zip, dest):
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
        try:
            processArgs = helpers.getCobanBinFolder + "7z.exe e " + zip + " -o" + dest + " -y"
            helpers.infoMessage("Unzipping " + zip + " to " + dest)
            runProcess = run(processArgs, stdout=DEVNULL, stderr=DEVNULL)
            helpers.successMessage("Successfully unzipped " + zip + " to " + dest)
        except WindowsError or PermissionError or FileNotFoundError as e:
            Logger.new(e).logError()
            exit()

    def cleanup(self, packageName=""):
        packagesPath = helpers.getCobanPath+"\\packages\\"+packageName

        if packageName != "":
            return self.removeDir(packagesPath)


        for i in helpers.installedApps()["installedApps"]:
            path = packagesPath+i
            if self.fileExists(path):
                self.removeDir(path)
                helpers.successMessage("Removed: " + i)

        for i in os.listdir(packagesPath):
            path = packagesPath+i
            if not i in helpers.installedApps()["installedApps"]:
                self.removeDir(path)
                helpers.successMessage("Removed: "+i)
import os, helpers, zipfile
from shutil import rmtree
from Logger import Logger
from subprocess import run, DEVNULL
from Logger import Logger as log
from json import dumps
from core import JsonParser as js
class Manager:
    def fileExists(path=""):
        try:
            if os.path.exists(path):
                return True
            else:
                return False
        except FileNotFoundError as e:
            helpers.errorMessage(e.strerror)
            exit()

    def createFolder(path):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except Exception as e:
            helpers.errorMessage(e.strerror)
            exit()
    def createFile(path, content =""):
        try:
            if not os.path.exists(path):
                with open(path, "w") as f:
                    f.write(content)
                    f.close()
        except Exception as e:
            log.new(e).logError()
            exit()

    def createJsonFile(self, path, withDict = {}):
        try:
            self.createFile(dumps(withDict))
        except FileNotFoundError or PermissionError or Exception as e:
            log.new(e).logError()
            helpers.errorMessage(e)

    def removeDir(self, path):
        if self.fileExists(path):
            try:
                rmtree(path)
                os.removedirs(path)
            except FileNotFoundError or WindowsError or PermissionError or Exception as e:
                helpers.errorMessage(e.strerror, True)
                exit()
        else:
            helpers.infoMessage("Path does not exists while trying to remove it: "+path, True)

    def extractZip(zip, dest):
        try:
            zf = zipfile.ZipFile(zip, "r")
            zf = zipfile.ZipFile.extractall(dest)
        except WindowsError or PermissionError or FileNotFoundError as e:
            Logger.new(e).logError()
            helpers.errorMessage(e.strerror)
            exit()

    def extract7z(zip, dest):
        try:
            processArgs = helpers.getCobanBinFolder+"7z.exe e "+zip+" -o"+dest+" -y"
            runProcess = run(processArgs, stdout=DEVNULL, stderr=DEVNULL)
        except WindowsError or PermissionError or FileNotFoundError as e:
            Logger.new(e).logError()
            helpers.errorMessage(e.strerror)
            exit()
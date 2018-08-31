from core import FileManager
import os
import helpers
from sys import exit

class main():
    def __init__(self):
        self.packageName = None
        self.rawPackageName = None
        if self.isPackgable():
            self.findInstallationScript()
            self.generateZip()

    def isPackgable(self):
        if os.path.exists(path=os.getcwd()+"\\.packagable"):
            return True
        else:
            helpers.errorMessage(
                "This path does not include any packagable packages.")
            helpers.errorMessage("Make sure you are in same directory.")
            return False

    def generateZip(self):
        path = os.getcwd()
        zipFile = self.packageName+".zip"
        ignoreFiles = [
            ".packagable",
            '.package/',
            zipFile
        ]

        makeZip = FileManager.Manager().makeZip(
            path, self.packageName + ".zip", ignoreFiles)

        if makeZip:
            helpers.successMessage("Packed your package at: {0}".format(
                os.getcwd()+"\\"+zipFile))
            helpers.successMessage(
                "You can push it by using argumant '--push' while you are in same directory.")

    def findInstallationScript(self):
        list = os.listdir(os.getcwd())

        for i in list:
            if i.endswith(".cb"):
                self.rawPackageName = i
                self.packageName = i.split(".")[0]

from . import installPackage
from core import JsonParser as json
import subprocess
import helpers
import os
from core import http
from core import FileManager as file
from Logger import Logger as log
from sys import exit

class main(installPackage.main):

    def test(self):
        if self.agreement() == True:
            if not self.isInstalled():
                self.__change_attrs()
                if self.isInstallable():
                    self.download()
                    self.checkHash(True)
                    if self.checkForDependencies():
                        self.downloadDependencies()
                    self.beginAction()
                    if self.valid_exit_code():
                        helpers.successMessage(
                            "Successfull! Test was successfull, you can now push your package to our server.")
                        file.Manager().createFile(".tested", "True", True)
                    else:
                        helpers.errorMessage(
                            "Aborting! Program exited with unexcepted exit code: "+str(self.exit_code))
                        return False
                else:
                    exit(
                        "This file type is not supported. Create issue if you really think it should.")
            else:
                helpers.messages("info", "alreadyInstalled", self.packageName)
        else:
            exit("You need to accept to contiune installation.")

    def __change_attrs(self):
        createHiddenPackageFolder = file.Manager().createFolder(".package", True)
        file.Manager().extractZip(self.packageName, ".package/")
        self.__find_installation_script()
        self.scriptFile = self.parser.fileToJson(os.path.abspath(".package/"+self.packageName+".cb"))["packageArgs"]
        self.packagePathWithoutExt = os.path.abspath(".package/{0}".format(self.packageName))

    def __find_installation_script(self):
        for i in os.listdir(".package"):
            if i.endswith(".cb"):
                self.packageName = i.split(".")[0]

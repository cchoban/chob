import repo, helpers
from core import http, FileManager, JsonParser
from Logger import Logger as log
from . import doctor
import re


class main:
    def __init__(self):
        pass

    def update(self):
        helpers.infoMessage("Updating repo if needed " + repo.repos()["programList"])
        # TODO: if needed check for file size
        try:
            http.Http.download(http.Http, repo.repos()["programList"], helpers.getCobanPath + "\\programList", "json")
        except Exception as e:
            log.new(e).logError()

    def doctor(self):
        self.update()
        doc = doctor.doctor()
        doc.createFolders()
        doc.validateJsonFiles()

        helpers.successMessage("Fixed problems..")

    def cleanLeftOvers(self):
        fileManager = FileManager.Manager().cleanup()

    def packages(self):
        self.update()
        js = helpers.installedApps()["installedApps"]
        return js

    def listPackages(self, local):
        if local == True:
            packages = helpers.installedApps()["installedApps"]
        else:
            packages = self.packages()
        for i in packages:
            print(i)

    def searchInPackages(self, packageName):
        for i in self.packages():

            regex = re.search(packageName.lower(), i.lower())

            if regex:
                helpers.successMessage("Found this package(s): ")
                print(i)

    def downloadDeps(self):
        doctor.doctor().downloadDependencies()

    def downloadScript(self, packageName):
        packageUrl = helpers.programList()[packageName]

        if not FileManager.Manager().fileExists(helpers.packageInstallationPath + packageName):
            FileManager.Manager().createFolder(helpers.packageInstallationPath + packageName)
        helpers.infoMessage("Downloading Installation Script of: " + packageName + ".cb")

        http.Http.download(http.Http, packageUrl,
                           helpers.packageInstallationPath + packageName + "\\" + packageName, "cb")

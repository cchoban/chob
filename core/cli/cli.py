import repo
import helpers
from core import http, FileManager
from packageCreator import creator, pack, push, auth
from Logger import Logger as log
from . import doctor
import re


class main:

    def __init__(self):
        pass

    def packageGenerator(self, packageName, generateFlatFileOnly=False):
        # TODO: bunu kendi classina tasi
        print(generateFlatFileOnly)
        if generateFlatFileOnly:
            cls = creator.generatePackage(packageName, generateFlatFileOnly)
            json = cls.generateJson()
            cls.writeToFile(json)
        else:
            cls = creator.generatePackage(packageName, False)
            cls.getAnswers()
            cls.generateJson()
            cls.writeToFile()

    def packit(self):
        return pack.main()

    def push(self):
        if auth.main().keyExists():
            return push.main()
        else:
            helpers.errorMessage(
                "You don't have authentication key. Please get one from {0}. You can activate it with --authentication".format(repo.repos()["website"]))

    def auth(self, token):
        return auth.main(True, token)

    def update(self):
        helpers.infoMessage("Updating repo if needed " +
                            repo.repos()["programList"])
        # TODO: if needed check for file size
        try:
            http.Http.download(http.Http, repo.repos()[
                               "programList"], helpers.getCobanPath + "\\programList", "json")
        except Exception as e:
            log.new(e).logError()

    def doctor(self):
        doc = doctor.doctor()
        doc.createFolders()
        doc.createFiles()
        doc.validateJsonFiles()
        self.update()
        helpers.successMessage("Fixed problems..")

    def cleanLeftOvers(self):
        fileManager = FileManager.Manager().cleanup()

    def packages(self):
        self.update()
        js = helpers.programList()
        return js

    def listPackages(self, local):
        if local == True:
            packages = helpers.installedApps()["installedApps"]
        else:
            packages = self.packages()
        for i in packages:
            print(i)

    def searchInPackages(self, packageName):
        foundPackages = []
        packages = self.packages()
        for package in packageName:
            for i in packages:
                regex = re.search(package.lower(), i.lower())

                if regex:
                    foundPackages.append(i)

        if len(foundPackages) > 0:
            helpers.successMessage("Found this package(s): ")
            for i in foundPackages:
                print(i)

    def downloadDeps(self):
        doctor.doctor().downloadDependencies()

    def downloadScript(self, packageName):
        packageUrl = helpers.programList()[packageName]

        if not FileManager.Manager().fileExists(helpers.packageInstallationPath + packageName):
            FileManager.Manager().createFolder(helpers.packageInstallationPath + packageName)
        helpers.infoMessage(
            "Downloading Installation Script of: " + packageName + ".cb")

        http.Http.download(http.Http, packageUrl,
                           helpers.packageInstallationPath + packageName + "\\" + packageName, "cb")
    def version(self):
        version_path = helpers.getCobanPath+"\\version.txt"
        if FileManager.Manager().fileExists(version_path):
            with open(version_path, "r") as f:
                helpers.successMessage("Choban Package Manager")
                helpers.infoMessage("Version "+f.read())
                f.close()
